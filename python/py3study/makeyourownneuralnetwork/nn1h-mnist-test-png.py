import nw
import numpy
import imageio
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open('nn1h-mnist-784-200-10', 'rb') as fp:
    n = nw.NN1h()
    n.load(fp)

    img_array = imageio.imread(os.path.join(BASE_DIR, '../data/g9.png'), as_gray=True)

    img_data = 255.0 - img_array.reshape(784)
    img_data = (img_data / 255.0 * 0.99) + 0.01

    inputs = img_data
    outputs = n.query(inputs)
    label = numpy.argmax(outputs)

    print(label)



