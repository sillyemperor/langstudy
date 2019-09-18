import numpy
import nw
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# number of input, hidden and output nodes
input_nodes = 784
hidden1_nodes = 200
hidden2_nodes = 200
output_nodes = 10

# learning rate
learning_rate = 0.1

# create instance of neural network
n = nw.NN2h(input_nodes,hidden1_nodes,hidden2_nodes,output_nodes, learning_rate)

# load the mnist training data CSV file into a list
training_data_file = open(os.path.join(BASE_DIR, "../data/mnist_train.csv"), 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()

# train the neural network

# epochs is the number of times the training data set is used for training
epochs = 5

for e in range(epochs):
    # go through all records in the training data set
    for record in training_data_list:
        # split the record by the ',' commas
        all_values = record.split(',')
        # scale and shift the inputs
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        # create the target output values (all 0.01, except the desired label which is 0.99)
        targets = numpy.zeros(output_nodes) + 0.01
        # all_values[0] is the target label for this record
        targets[int(all_values[0])] = 0.99
        n.train(inputs, targets)
        pass
    pass

with open('nn2h-mnist-784-200-10', 'wb') as fp:
    n.save(fp)

