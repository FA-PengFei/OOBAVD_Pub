import array
import os

import numpy as np
from PIL import Image

import cv2
from numba import njit


# @njit
def execute(temp_left, temp_right, bi_gram_disbn):
    temmp = temp_left + temp_right  # im11_hex[k1][2:4] + im11_hex[k1 + 1][2:4]
    print(99, temmp, temp_left, temp_right)
    exit()
    hexx = int(temmp, 16)
    bi_gram_disbn[hexx] = bi_gram_disbn[hexx] + 1


# @profile
def get_bigram_dct_image(binfile):
    """
    r_type :   0- unnormalized
               1- max-normalised
    """
    ln = os.path.getsize(os.path.abspath(binfile))
    file_size = ln / 1024
    f = open(binfile, 'rb')
    if file_size < 10:
        col_size = 32
    else:
        if file_size >= 10 and file_size < 30:
            col_size = 64
        else:
            if file_size >= 30 and file_size < 60:
                col_size = 128
            else:
                if file_size >= 60 and file_size < 100:
                    col_size = 256
                else:
                    if file_size >= 100 and file_size < 200:
                        col_size = 384
                    else:
                        if file_size >= 200 and file_size < 500:
                            col_size = 512
                        else:
                            if file_size >= 500 and file_size < 1000:
                                col_size = 768
                            else:
                                col_size = 1024
    rem = ln % col_size
    if ln == rem:
        assert ln < 1024, str(ln)
        rem = 0
    a = array.array('B')
    a.fromfile(f, ln - rem)
    f.close()
    if ln < col_size:
        g = np.expand_dims(
            np.pad(a, ((0, col_size - ln),), mode='constant'), 0)
    else:
        g = np.reshape(a, (-1, col_size))
    im11 = np.uint8(g)
    im11_vect = im11.reshape((1, im11.shape[0] * im11.shape[1]))[0]
    #vhex = np.vectorize(hex)
    #im11_hex = vhex(im11_vect)
    bi_gram_disbn = np.zeros(int('ffff', 16) + 1)

    #hexxes = []
    # for k1 in range(len(im11_hex) - 1):
    #    temmp = im11_hex[k1][2:4] + im11_hex[k1 + 1][2:4]
    #    hexx = int(temmp, 16)
    #    hexxes.append(hexx)
    #    bi_gram_disbn[hexx] += 1
    # execute(im11_hex[k1][2:4], im11_hex[k1 + 1][2:4], bi_gram_disbn)
#    else:

    bi_gram_disbn = np.zeros(int('ffff', 16) + 1)
    temmp = im11_vect[1:].astype(np.uint16)
    temmp2 = im11_vect[:-1].astype(np.uint16)
    temmp += np.where(temmp < 0x10, temmp2 * 0x10, temmp2 * 0x100)
    np.add.at(bi_gram_disbn, temmp, 1)

    bi_gram_disbn[0] = 0
    temp_norm = bi_gram_disbn / bi_gram_disbn.max()
    img_2d = np.reshape(temp_norm, (256, 256))
    dst = cv2.dct(img_2d)
    dst_norm = (dst - dst.min()) / (dst.max() - dst.min())
    img_tran = np.uint8(dst_norm * 255.0)
    im = np.array(img_tran)
    return im
