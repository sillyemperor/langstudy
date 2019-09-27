import pickle
import numpy as np
from scipy import signal as sg
import imageio
import math
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
M = 0xffffff


def norm(ar):
    return 255. * np.absolute(ar) / np.max(ar)


def unpickle(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict


def load_raw(file):
    dmap = unpickle(file)
    label_ids = dmap[b'fine_labels']
    for id, data in enumerate(dmap[b'data']):
        red = data[:1024]
        green = data[1024:2048]
        blue = data[2048:]

        mix = []
        for i in range(1024):
            p = red[i] << 16 | green[i] << 8 | blue[i]
            mix.append(int(p * 255 / M))
        yield (label_ids[id], mix)


def load(file):
    with open(file, 'rb') as fo:
        return pickle.load(fo)


def sharp(img):
    img = sg.convolve(img, [
        [-1, -1, -1, -1, -1],
        [-1, 2, 2, 2, -1],
        [-1, 2, 8, 2, -1],
        [-1, 2, 2, 2, -1],
        [-1, -1, -1, -1, -1],
    ], mode='same')
    # img = sg.convolve(img, [
    #                         [-1., -1., -1.],
    #                         [-1., 8., -1.],
    #                         [-1., -1., -1.],
    #                              ], mode='same')

    img = norm(img)
    return img


def array2img(ar, gray=False):
    M = 0xffffff
    red = ar[:1024]
    green = ar[1024:2048]
    blue = ar[2048:]
    mix = []
    for i in range(red.size):
        if gray:
            p = red[i] << 16 | green[i] << 8 | blue[i]
            mix.append(int(p * 255 / M))
        else:
            mix.append((red[i], green[i], blue[i]))
    mix = np.array(mix)
    if gray:
        return mix.reshape(32, 32)
    else:
        return mix.reshape(32, 32, 3)


def save(img, file_name):
    imageio.imwrite(file_name, img)


def save_jpg(first_array, file_name, mode='normal', sharpen=False):
    red = first_array[:1024]
    green = first_array[1024:2048]
    blue = first_array[2048:]

    # print(red.size)
    # print(green.size)
    # print(blue.size)

    M = 0xffffff

    mix = []
    for i in range(red.size):
        if 'normal' is mode:
            mix.append((red[i], green[i], blue[i]))
        else:
            p = red[i] << 16 | green[i] << 8 | blue[i]
            mix.append(int(p * 255 / M))

    mix = np.array(mix)
    # print(mix.shape)

    if 'normal' is mode:
        mix = mix.reshape(32, 32, 3)
    else:
        mix = mix.reshape(32, 32)

    if sharpen:
        mix = sharp(mix)

    imageio.imwrite(file_name, mix)


from NumPyCNN import *


def prepare(ar):
    n = ar.size
    d = int(math.sqrt(n))
    img = ar.reshape(d, d)
    l1_filter = np.zeros((2, 3, 3))
    l1_filter[0, :, :] = np.array([[[-1, 0, 1],
                                    [-1, 0, 1],
                                    [-1, 0, 1]]])
    l1_filter[1, :, :] = np.array([[[1, 1, 1],
                                    [0, 0, 0],
                                    [-1, -1, -1]]])
    l1_feature_map = conv(img, l1_filter)
    l1_feature_map_relu = relu(l1_feature_map)
    l1_feature_map_relu_pool = pooling(l1_feature_map_relu, 2, 2)
    return np.array(l1_feature_map_relu_pool).reshape(l1_feature_map_relu_pool.size)


def array2rgb(ar):
    size = len(ar)/3
    red = ar[:size]
    green = ar[size:size*2]
    blue = ar[size*2:]

    for i in range(size):
        yield red[i], green[i], blue[i]


def array2gray(ar):
    for r, g, b in array2rgb(ar):
        p = r << 16 | g << 8 | b
        yield p * 0.99 / M


def read_cifar100(train=True):
    # batch_label,coarse_labels,data,filenames,fine_labels
    meta = unpickle(os.path.join(BASE_DIR, '../data/cifar-100-python/meta'))
    _dict = unpickle(os.path.join(BASE_DIR, f'../data/cifar-100-python/{"train" if train else "test"}'))
    meta_label_names = meta[b'fine_label_names']
    filenames = _dict[b'filenames']
    labels = _dict[b'fine_labels']
    datas = _dict[b'data']
    n = len(datas)
    for i, data in enumerate(datas):
        id = labels[i]
        if i % 1000:
            print(f'{int(i*100/n)}%')
        yield id, meta_label_names[id].decode(), filenames[id].decode(), data


def read_cifar10(train=True):
    # batch_label,coarse_labels,data,filenames,fine_labels
    meta = unpickle(os.path.join(BASE_DIR, '../data/cifar-10-batches-py/batches.meta'))
    meta_label_names = meta[b'label_names']

    if train:
        for i in range(1, 6):
            _dict = unpickle(os.path.join(BASE_DIR, f'../data/cifar-10-batches-py/data_batch_{i}'))
            filenames = _dict[b'filenames']
            labels = _dict[b'labels']
            datas = _dict[b'data']
            for i, data in enumerate(datas):
                id = labels[i]
                yield id, meta_label_names[id].decode(), filenames[id].decode(), data
    else:
        _dict = unpickle(os.path.join(BASE_DIR, f'../data/cifar-10-batches-py/test_batch'))
        filenames = _dict[b'filenames']
        labels = _dict[b'labels']
        datas = _dict[b'data']
        for i, data in enumerate(datas):
            id = labels[i]
            yield id, meta_label_names[id].decode(), filenames[id].decode(), data


def read_cifar100_gray(name):
    with open(os.path.join(BASE_DIR, f'../data/cifar-100-python/{name}_gray'), 'rb') as fp:
        array = pickle.load(fp)
        return array


def transform100():
    #  生成训练数据，加快载入速度
    train_data = [(id, name, fname, array2gray(data)) for id, name, fname, data in read_cifar100(train=True)]
    with open(os.path.join(BASE_DIR, '../data/cifar-100-python/train_gray'), 'wb') as fp:
        pickle.dump(train_data, fp)
    print('transform train gray')

    test_data = [(id, name, fname, array2gray(data)) for id, name, fname, data in read_cifar100(train=False)]
    with open(os.path.join(BASE_DIR, '../data/cifar-100-python/test_gray'), 'wb') as fp:
        pickle.dump(test_data, fp)
    print('transform test gray')


if __name__ == '__main__':
    transform100()
