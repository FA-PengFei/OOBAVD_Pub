<<<<<<< HEAD
import array
import os

import numpy as np

=======
>>>>>>> ac6e4a2dd26ed6a1ff9d224b0ca01a6d33efeb66


def get_byteplot_image(file_loc):
    ln = os.path.getsize(file_loc)
    file_size = ln / 1024
    f = open(file_loc, 'rb')
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
    im = np.array(g)
    return im
