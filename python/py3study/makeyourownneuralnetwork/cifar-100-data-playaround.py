import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import pprint
import numpy as np
import imageio
from scipy import signal as sg
import cifar


meta = cifar.unpickle(os.path.join(BASE_DIR, '../data/cifar-100-python/meta'))

# pprint.pprint(meta)

meta_label_names = meta[b'fine_label_names']

# pprint.pprint(len(meta_label_names))
#
test = cifar.unpickle(os.path.join(BASE_DIR, '../data/cifar-100-python/test'))
# pprint.pprint(test) #batch_label,coarse_labels,data,filenames,fine_labels

# pprint.pprint(test.keys())  # dict_keys([b'filenames', b'batch_label', b'fine_labels', b'coarse_labels', b'data'])
#
# label_ids = test[b'fine_labels']
# pprint.pprint([min(label_ids), max(label_ids)])
# label_names = list(map(lambda i:meta_label_names[i], label_ids))
# # pprint.pprint(label_names)
#
# mdata = test[b'data'];

# for id in range(mdata.size):
#     cifar.save_jpg(mdata, label_names, id)
#     break

train = cifar.unpickle(os.path.join(BASE_DIR, '../data/cifar-100-python/train'))
pprint.pprint(train[b'fine_labels'])