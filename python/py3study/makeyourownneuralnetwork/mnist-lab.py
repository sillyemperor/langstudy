import nw
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import time
import numpy as np

# load the mnist training data CSV file into a list
training_data_file = open(os.path.join(BASE_DIR, "../data/mnist_train.csv"), 'r')
train_datas = training_data_file.readlines()
training_data_file.close()

test_data_file = open(os.path.join(BASE_DIR, "../data/mnist_test.csv"), 'r')
test_datas = test_data_file.readlines()
test_data_file.close()

train_datas = [(int(record.split(',')[0]), (np.asfarray(record.split(',')[1:]) / 255.0 * 0.99) + 0.01) for record in train_datas]
test_datas = [(int(record.split(',')[0]), (np.asfarray(record.split(',')[1:]) / 255.0 * 0.99) + 0.01) for record in test_datas]

nw.train_test(nw.NNnh(200),
              train_datas=train_datas,
              test_datas=test_datas,
              target_num=10,
              epochs=3
              )

# 0 0.021269481237146424 94.81% 16.97789716720581s
# 1 0.01805896751321641 96.17% 16.191657066345215s
# 2 0.020635117003390557 96.55% 16.317293882369995s
# NNnh(784-(200-1)-10-0.1) 3 49.48684811592102