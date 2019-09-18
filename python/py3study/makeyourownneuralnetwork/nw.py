import numpy
# scipy.special for the sigmoid function expit()
import scipy.special
import pickle

# neural network with 1 hiden layer
class NN1h:

    # initialise the neural network
    def __init__(self, inputnodes=5, hiddennodes=5, outputnodes=5, learningrate=0.1):
        # set number of nodes in each input, hidden, output layer
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to node j in the next layer
        # w11 w21
        # w12 w22 etc
        self.wih = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        # learning rate
        self.lr = learningrate

        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

        pass

    def save(self, f):
        pickle.dump((
            self.inodes, self.hnodes, self.onodes, self.wih, self.who, self.lr
        ), f)

    def load(self, f):
        self.inodes, self.hnodes, self.onodes, self.wih, self.who, self.lr = pickle.load(f)

    # train the neural network
    def train(self, inputs_list, targets_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = numpy.dot(self.who.T, output_errors)

        # update the weights for the links between the hidden and output layers
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                                        numpy.transpose(hidden_outputs))

        # update the weights for the links between the input and hidden layers
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)),
                                        numpy.transpose(inputs))

        pass

    # query the neural network
    def query(self, inputs_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs


# neural network with 1 hiden layer
class NN2h:

    # initialise the neural network
    def __init__(self, inputnodes=5, hidden1nodes=5, hidden2nodes=5, outputnodes=5, learningrate=0.1):
        # set number of nodes in each input, hidden, output layer
        self.inodes = inputnodes
        self.h1nodes = hidden1nodes
        self.h2nodes = hidden2nodes
        self.onodes = outputnodes

        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to node j in the next layer
        # w11 w21
        # w12 w22 etc
        self.wih1 = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.h1nodes, self.inodes))
        self.wh1h2 = numpy.random.normal(0.0, pow(self.h1nodes, -0.5), (self.h1nodes, self.h2nodes))
        self.wh2o = numpy.random.normal(0.0, pow(self.h2nodes, -0.5), (self.onodes, self.h2nodes))

        # learning rate
        self.lr = learningrate

        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

        pass

    def save(self, f):
        pickle.dump((
            self.inodes, self.h1nodes, self.h2nodes, self.onodes, self.wih1, self.wh1h2, self.wh2o, self.lr
        ), f)

    def load(self, f):
        self.inodes, self.h1nodes, self.h2nodes, self.onodes, self.wih1, self.wh1h2, self.wh2o, self.lr = pickle.load(f)

    # train the neural network
    def train(self, inputs_list, targets_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden1_inputs = numpy.dot(self.wih1, inputs)
        hidden1_outputs = self.activation_function(hidden1_inputs)

        hidden2_inputs = numpy.dot(self.wh1h2, hidden1_outputs)
        # calculate the signals emerging from hidden layer
        hidden2_outputs = self.activation_function(hidden2_inputs)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.wh2o, hidden2_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = numpy.dot(self.wh2o.T, output_errors)

        # update the weights for the links between the hidden and output layers
        self.wh2o += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                                        numpy.transpose(hidden2_outputs))

        # update the weights for the links between the input and hidden layers
        self.wh1h2 += self.lr * numpy.dot((hidden_errors * hidden2_outputs * (1.0 - hidden2_outputs)),
                                        numpy.transpose(hidden1_outputs))

        self.wih1 += self.lr * numpy.dot((hidden_errors * hidden1_outputs * (1.0 - hidden1_outputs)),
                                        numpy.transpose(inputs))

        pass

    # query the neural network
    def query(self, inputs_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden1_inputs = numpy.dot(self.wih1, inputs)
        hidden1_outputs = self.activation_function(hidden1_inputs)

        # calculate the signals emerging from hidden layer
        hidden2_inputs = numpy.dot(self.wh1h2, hidden1_outputs)
        hidden2_outputs = self.activation_function(hidden2_inputs)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.wh2o, hidden2_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs
