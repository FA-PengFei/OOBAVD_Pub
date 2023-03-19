import csv
import shutil

filename = 'samples.csv'
images_loc = 'byteplot_and_dct'


def get_class_arr():
    with open(filename) as samples_csv:
        reader = csv.reader(samples_csv, delimiter=',')
        ret_arr = []
        next(reader, None)
        for row in reader:
            res = 0
            if row[6] == 'Blacklist':
                res = 1
            ret_arr.append([row[0], res])
        return ret_arr


def sort_by_class(arr):
    for item in arr:
        if item[1] == 0:
            shutil.copy(
                f'{images_loc}/{item[0]}.png', f'categorized_byteplot_and_dct/notmalware/{item[0]}.png')
        else:
            shutil.copy(f'{images_loc}/{item[0]}.png',
                        f'categorized_byteplot_and_dct/malware/{item[0]}.png')

    return


if __name__ == "__main__":
    arr = get_class_arr()
    sort_by_class(arr)
