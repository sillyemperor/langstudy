import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import pprint
import numpy as np
import cifar

meta = cifar.unpickle(os.path.join(BASE_DIR, '../data/cifar-10-batches-py/batches.meta'))
# pprint.pprint(meta)

label_names = meta[b'label_names']

test = cifar.unpickle(os.path.join(BASE_DIR, '../data/cifar-10-batches-py/test_batch'))

# pprint.pprint(test)
labels = test[b'labels']
# print(labels)
label_names = list(map(lambda i:label_names[i], labels))

datas = test[b'data']
# pprint.pprint(test)
#
# data_batch_1 = cifar.unpickle(os.path.join(BASE_DIR, '../data/cifar-10-batches-py/data_batch_1'))
# pprint.pprint(data_batch_1)
#
# data = data_batch_1[b'data']

from NumPyCNN import *

for id, data in enumerate(datas):
    img = cifar.array2img(data, gray=True)
    l1_filter = np.zeros((2,3,3))
    l1_filter[0, :, :] = np.array([[[-1, 0, 1],
                                       [-1, 0, 1],
                                       [-1, 0, 1]]])
    l1_filter[1, :, :] = np.array([[[1, 1, 1],
                                       [0, 0, 0],
                                       [-1, -1, -1]]])
    l1_feature_map = conv(img, l1_filter)
    cifar.save(l1_feature_map[:, :, 0], '~/tmp/nn/a.jpg')
    l1_feature_map_relu = relu(l1_feature_map)
    cifar.save(l1_feature_map_relu[:, :, 0], '~/tmp/nn/b.jpg')
    l1_feature_map_relu_pool = pooling(l1_feature_map_relu, 2, 2)

    cifar.save(l1_feature_map_relu_pool[:, :, 0], '~/tmp/nn/c.jpg')
    break


