import imageio
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import numpy as np
from scipy import signal
from scipy import misc

lena = imageio.imread(os.path.join(BASE_DIR, '../data/lena_std.tif'))
print(lena.shape)
imageio.imwrite('~/tmp/lena.jpg', lena)

x = np.array(lena)
print(x.shape)
# print(x.min(), x.max())
gray_lena = x.dot([0.0039, 0.0039, 0.0039])
# print(x.min(), x.max())
print(x.shape)
imageio.imwrite('~/tmp/lena-gray.jpg', gray_lena)

scharr = np.array([[ -3-3j, 0-10j,  +3 -3j],
                    [-10+0j, 0+ 0j, +10 +0j],
                    [ -3+3j, 0+10j,  +3 +3j]]) # Gx + j*Gy
x = signal.convolve2d(gray_lena, scharr, boundary='symm', mode='same')
print(x.shape)
imageio.imwrite('~/tmp/lena-conv1.jpg', x)


scharr = np.array([[ -1, -1,  -1],
                    [-1, 8, -1],
                    [ -1,-1,  -1]]) # Gx + j*Gy
x = signal.convolve2d(gray_lena, scharr, boundary='symm', mode='same')
print(x.shape)
imageio.imwrite('~/tmp/lena-conv2.jpg', x)

scharr = np.array([
                    [ -1, -1,  -1, -1, -1],
                    [ -1, 2,  2, 2, -1],
                    [ -1, 2,  8, 2, -1],
                    [ -1, 2,  2, 2, -1],
                    [ -1, -1,  -1, -1, -1],
                ]) # Gx + j*Gy
x = signal.convolve2d(gray_lena, scharr, boundary='symm', mode='same')
print(x.shape)
imageio.imwrite('~/tmp/lena-conv3.jpg', x)

scharr = np.array([[ 0, 1,  0],
                    [1, -4, 1],
                    [ 0,1,  0]]) # Gx + j*Gy
x = signal.convolve2d(gray_lena, scharr, boundary='symm', mode='same')
print(x.shape)
imageio.imwrite('~/tmp/lena-conv4.jpg', x)


scharr = np.array([[ -1, -1,  0],
                    [-1, 0, 1],
                    [0, 1,  1]]) # Gx + j*Gy
x = signal.convolve2d(gray_lena, scharr, boundary='symm', mode='same')
print(x.shape)
imageio.imwrite('~/tmp/lena-conv5.jpg', x)