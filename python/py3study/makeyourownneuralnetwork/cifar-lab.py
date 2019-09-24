import numpy as np
import nw
import cifar


def array2gray(ar):
    M = 0xffffff
    red = ar[:1024]
    green = ar[1024:2048]
    blue = ar[2048:]

    mix = []
    for i in range(1024):
        p = red[i] << 16 | green[i] << 8 | blue[i]
        mix.append(p * 0.99 / M)
    # print(mix)
    r = cifar.prepare(np.array(mix))
    # print(mix, r)
    return r

###############cifar100###############
# train_datas = list(cifar.read_cifar100(True, filter=array2gray))
# print('load train datas')
#
#
# test_datas = list(cifar.read_cifar100(False, filter=array2gray))
# print('load test datas')
#
# train_datas = [(id, img) for id, name, fname, img in train_datas]
# test_datas = [(id, img) for id, name, fname, img in test_datas]
#
# nw.train_test(nw.NNnh(300),
#               train_datas=train_datas,
#               test_datas=test_datas,
#               target_num = 100,
#               epochs=3
#               )
# gray
# 0 0.09992193925616528 3.18 34.550604820251465
# 1 0.043000412105076054 5.08 36.30843210220337
# 2 0.016608539668518576 6.15 37.35742378234863
# NNnh(1024-(300-1)-100-0.1) 3 108.21646070480347

# conv
# 0 0.023143823210030327 11.22% 17.18569803237915s
# 1 0.021163569528167427 13.09% 30.12927007675171s
# 2 0.012188609980089244 13.85% 29.40558695793152s
# NNnh(450-(300-1)-100-0.1) 3 76.72055506706238

###############cifar10###############
train_datas = [(id, array2gray(img)) for id, name, fname, img in cifar.read_cifar10(True)]
print('load train datas')

test_datas = [(id, array2gray(img)) for id, name, fname, img in cifar.read_cifar10(False)]
print('load test datas')

nw.train_test(nw.NNnh(300),
              train_datas=train_datas,
              test_datas=test_datas,
              target_num = 10,
              epochs=3
              )
# conv
# 0 0.05985657847266848 39.45% 12.384026050567627s
# 1 0.029691063197885868 42.49% 12.273535013198853s
# 2 0.02643289510716314 43.12% 12.356266975402832s
# NNnh(450-(300-1)-10-0.1) 3 37.01382803916931
