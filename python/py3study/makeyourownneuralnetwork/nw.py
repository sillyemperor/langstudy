import numpy as np
# scipy.special for the sigmoid function expit()
import scipy.special
import pickle

# neural network with 1 hiden layer
class NN1h:
    # initialise the neural network
    def __init__(self, hiddennodes=5, learningrate=0.1):
        # set number of nodes in each input, hidden, output layer
        self.inodes = None
        self.hnodes = hiddennodes
        self.onodes = None
        # learning rate
        self.lr = learningrate

        # activation function is the sigmoid function
        self.activation_function = scipy.special.expit

        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to node j in the next layer
        # w11 w21
        # w12 w22 etc
        self.wih = None
        self.who = None

    def __str__(self):
        return f'NN1h({self.inodes}-{self.hnodes}-{self.onodes}-{self.lr})'

    def save(self, f):
        pickle.dump((
            self.inodes, self.hnodes, self.onodes, self.wih, self.who, self.lr
        ), f)

    def load(self, f):
        self.inodes, self.hnodes, self.onodes, self.wih, self.who, self.lr = pickle.load(f)

    # train the neural network
    def train(self, inputs_list, targets_list):
        if not self.inodes:
            self.inodes = inputs_list.size
            self.onodes = targets_list.size
            self.wih = np.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
            self.who = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))
            # print(self)

        inputs, hidden_inputs, hidden_outputs, final_inputs, final_outputs = self.query(inputs_list)
        # print(final_outputs.argmax(), targets_list.argmax())
        targets = np.array(targets_list, ndmin=2).T
        # output layer error is the (target - actual)

        output_errors = targets - final_outputs
        self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                                        np.transpose(hidden_outputs))

        # update the weights for the links between the input and hidden layers
        hidden_errors = np.dot(self.who.T, output_errors)
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)),
                                        np.transpose(inputs))

        return output_errors

    # query the neural network
    def query(self, inputs_list):
        # convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T
        # print(inputs)
        # calculate signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs)
        # print(hidden_inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        # print(hidden_outputs)
        # calculate signals into final output layer
        final_inputs = np.dot(self.who, hidden_outputs)
        # print(final_inputs)

        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)
        # print(final_outputs)

        return inputs, hidden_inputs, hidden_outputs, final_inputs, final_outputs


class NNnh:
    def __init__(self, hnodes, hlayers=1, learningrate=.1):
        self.hlayers = hlayers
        self.hnodes = hnodes
        self.inodes = None
        self.onodes = None
        self.learningrate = learningrate
        self.activation_function = scipy.special.expit
        self.whh = []
        self.is_init_train = False

    def __str__(self):
        return f'NNnh({self.inodes}-({self.hnodes}-{self.hlayers})-{self.onodes}-{self.learningrate})'

    def query(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T
        # print(inputs_list, inputs)

        outputs_ar = [inputs]

        for wh in self.whh:
            inputs = np.dot(wh, inputs)
            inputs = self.activation_function(inputs)
            outputs_ar.append(inputs)

        return outputs_ar

    def train(self, inputs_list, targets_list):
        if not self.is_init_train:
            self.init_train(inputs_list, targets_list)

        outputs_ar = self.query(inputs_list)

        targets = np.array(targets_list, ndmin=2).T

        errors = None
        ei = None
        ei1 = None
        for i in range(len(self.whh)-1, -1, -1):
            oi1 = outputs_ar[i+1]
            oi = outputs_ar[i]
            if ei is None:
                ei = targets - oi1
                errors = ei
            else:
                ei = np.dot(wi1.T, ei1)
            ei1 = ei
            wi1 = self.whh[i]

            self.whh[i] += self.learningrate * np.dot((ei * oi1 * (1.0 - oi1)),
                                      np.transpose(oi))

        return errors

    def init_train(self, inputs_list, targets_list):
        self.inodes = inputs_list.size
        self.onodes = targets_list.size
        wih = np.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.whh.append(wih)

        for l in range(self.hlayers - 1):
            wl = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.hnodes))
            self.whh.append(wl)

        who = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))
        self.whh.append(who)

        self.is_init_train = True


def train_test(n, target_num, train_datas, test_datas, epochs=3):
    import time
    import numpy as np
    performance = 0
    for e in range(epochs):
        loss = .0
        t = time.time()
        for id_, inputs in train_datas:
            targets = np.zeros(target_num) + 0.01
            targets[id_] = 0.99
            errors = n.train(inputs, targets)
            # print(inputs, targets, errors)
            # return
            loss += errors.sum()
        t = time.time() - t
        performance += t
        loss /= len(train_datas)

        scorecard = []
        for id_, inputs in test_datas:
            outputs = n.query(inputs)[-1]
            label = outputs.argmax()
            if label == id_:
                scorecard.append(1)
            else:
                scorecard.append(0)

        scorecard_array = np.asarray(scorecard)
        r = scorecard_array.sum() * 100 / scorecard_array.size
        print(e, loss, f'{r}%', f'{t}s')
    print(str(n), epochs, performance)
