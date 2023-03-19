import argparse
import csv
import os
import sys
from multiprocessing.dummy import Pool
from pathlib import Path
from re import L

import tqdm
from matplotlib import pyplot as plt
from PIL import Image

from get_bigram_dct_image import *
from get_byteplot_image import *

filename = 'samples.csv'
samples_location = 'samples'
images_location = 'byteplot_and_dct'
total = 0
current = 0


def get_total(filename):
    with open(filename) as f:
        return len(f.readlines())


def get_sample_ids():
    with open(filename) as samples_csv:
        total_ids = []
        total = get_total(filename)
        reader = csv.reader(samples_csv, delimiter=",")
        next(reader, None)
        value = 0
        for row in reader:
            total_ids.append(row[0])

        return total_ids


def convert_to_img(sample_id):
    plot = get_bigram_dct_image(f'{samples_location}\{sample_id}')
    plt.imshow(plot, cmap="gray", vmin=0, vmax=255)
    plt.axis("off")
    plt.savefig(f'{images_location}\{sample_id}.png')
    # if(current % 100 == 0):
    #print(f"{current}/{total} {round(((current/total) * 100), 2)}%")
    #current += 1


def convert_to_img_pillow(sample_id):
    try:
        plot = get_bigram_dct_image(f'{samples_location}\{sample_id}')
        img = Image.fromarray(plot)
        img.save(f'{images_location}\{sample_id}.png')
    except:
        pass


def convert_to_byteplot(sample_id):
    try:
        plot = get_byteplot_image(f'{samples_location}\{sample_id}')
        img = Image.fromarray(plot)
        img = img.resize((256, 256))
        img.save(f'{images_location}\{sample_id}.png')
    except:
        pass


def convert_to_byteplot_and_dct(sample_id):
    try:
        dct_plot = get_bigram_dct_image(f'{samples_location}\{sample_id}')
        byteplot = get_byteplot_image(f'{samples_location}\{sample_id}')
        byteplot_img = Image.fromarray(byteplot)
        # idk how the behaviour would be so do the same as convert_to_byteplot
        byteplot_img = byteplot_img.resize((256, 256))
        resized_byteplot = np.array(byteplot_img)
        and_plot = np.logical_and(dct_plot, resized_byteplot)
        img = Image.fromarray(and_plot)
        img.save(f'{images_location}\{sample_id}.png')
    except:
        pass


def from_folder(filepath):
    filepath = os.path.join(Path.cwd(), filepath)
    filepaths = []
    for (root, dirs, files) in os.walk(filepath):
        for file in files:
            filepaths.append([os.path.join(root, file), file])

    return filepaths


def byteplot_filepaths(filepath):
    try:
        plot = get_byteplot_image(filepath[0])
        img = Image.fromarray(plot)
        img = img.resize((256, 256))
        img.save(f'{images_location}\{filepath[1]}.png')
    except:
        pass


def run_folder(folder_name):
    files = from_folder(folder_name)
    pool = Pool()
    for _ in tqdm.tqdm(pool.imap(byteplot_filepaths, files), total=len(files)):
        pass
    pool.close()
    sys.exit(0)


def run(format):
    total = get_total(filename)
    ids = get_sample_ids()
    pool = Pool()
    if format == 'dct':
        for _ in tqdm.tqdm(pool.imap(convert_to_img_pillow, ids), total=len(ids)):
            pass
        pool.close()
        sys.exit(0)

    if format == 'byteplot':
        for _ in tqdm.tqdm(pool.imap(convert_to_byteplot, ids), total=len(ids)):
            pass
        pool.close()
        sys.exit(0)
    if format == 'byteplot_dct':
        for _ in tqdm.tqdm(pool.imap(convert_to_byteplot_and_dct, ids), total=len(ids)):
            pass
        pool.close()
        sys.exit(0)

    sys.stderr.write("incorrect format specified: byteplot, dct, byteplot_dct")
    sys.exit(1)


if __name__ == "__main__":
    #total = get_total(filename)
    #ids = get_sample_ids()

    #pool = Pool()
    # for _ in tqdm.tqdm(pool.imap(convert_to_byteplot_and_dct, ids), total=len(ids)):
    #    pass
    # pool.close()
    parser = argparse.ArgumentParser(argument_default="--help")
    parser.add_argument('--csv', help="csv file with the malware ids")
    parser.add_argument('--input', help="input folder for malware samples")
    parser.add_argument('--output', help="output folder for proccessed images")
    parser.add_argument(
        '--format', help="format for image processing: byteplot, dct, byteplot_dct")
    parser.add_argument('--folder', help="Convert images from folder instead.")
    args = parser.parse_args()

    filename = args.csv
    samples_location = args.input
    images_location = args.output
#
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if len(args.folder) == 0:
        run(args.format)
    else:
        run_folder(args.folder)
