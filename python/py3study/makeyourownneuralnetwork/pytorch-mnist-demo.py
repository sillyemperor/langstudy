import torch
import torchvision
import torchvision.transforms as transforms
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, ), (0.5, )),
     ])

root = os.path.join(BASE_DIR, '../data/')
trainset = torchvision.datasets.MNIST(root=root, train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.MNIST(root=root, train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset,
                                         shuffle=False, num_workers=2)

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # print('input', x.shape)
        x = self.conv1(x)
        # print('conv', x.shape)
        x = F.relu(x)
        # print('relu', x.shape)
        x = self.pool(x)
        # print('pool', x.shape)

        x = self.conv2(x)
        # print('conv', x.shape)
        x = F.relu(x)
        # print('relu', x.shape)
        x = self.pool(x)
        # print('pool', x.shape)

        x = x.view(-1, 16 * 4 * 4)
        # print('view', x.shape)

        x = self.fc1(x)
        # print('Linear', x.shape)
        x = F.relu(x)
        # print('relu', x.shape)

        x = self.fc2(x)
        # print('Linear', x.shape)
        x = F.relu(x)
        # print('relu', x.shape)

        x = self.fc3(x)
        # print('Linear', x.shape)
        return x

# input torch.Size([1, 1, 28, 28])
# conv torch.Size([1, 6, 24, 24])
# relu torch.Size([1, 6, 24, 24])
# pool torch.Size([1, 6, 12, 12])
# conv torch.Size([1, 16, 8, 8])
# relu torch.Size([1, 16, 8, 8])
# pool torch.Size([1, 16, 4, 4])
# view torch.Size([1, 256])
# Linear torch.Size([1, 120])
# relu torch.Size([1, 120])
# Linear torch.Size([1, 84])
# relu torch.Size([1, 84])
# Linear torch.Size([1, 100])

net = Net()

criterion = nn.CrossEntropyLoss()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

for epoch in range(10):  # loop over the dataset multiple times

    net.train()
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 5000 == 4999:  # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 5000))
            running_loss = 0.0

    correct = 0
    total = 0
    net.eval()
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            outputs = net(images)

            _, predicted = torch.max(outputs.data, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'{correct} / {total}, {100 * correct / total}%')


#
# [1,  5000] loss: 0.531
# [1, 10000] loss: 0.151
# [1, 15000] loss: 0.103
# [1, 20000] loss: 0.088
# [1, 25000] loss: 0.085
# [1, 30000] loss: 0.078
# [1, 35000] loss: 0.061
# [1, 40000] loss: 0.060
# [1, 45000] loss: 0.063
# [1, 50000] loss: 0.067
# [1, 55000] loss: 0.058
# [1, 60000] loss: 0.061
# 9829 / 10000, 98.29%
# [2,  5000] loss: 0.038
# [2, 10000] loss: 0.034
# [2, 15000] loss: 0.041
# [2, 20000] loss: 0.044
# [2, 25000] loss: 0.040
# [2, 30000] loss: 0.046
# [2, 35000] loss: 0.039
# [2, 40000] loss: 0.042
# [2, 45000] loss: 0.042
# [2, 50000] loss: 0.035
# [2, 55000] loss: 0.039
# [2, 60000] loss: 0.043
# 9871 / 10000, 98.71%
# [3,  5000] loss: 0.019
# [3, 10000] loss: 0.023
# [3, 15000] loss: 0.024
# [3, 20000] loss: 0.028
# [3, 25000] loss: 0.026
# [3, 30000] loss: 0.028
# [3, 35000] loss: 0.025
# [3, 40000] loss: 0.030
# [3, 45000] loss: 0.032
# [3, 50000] loss: 0.029
# [3, 55000] loss: 0.033
# [3, 60000] loss: 0.025
# 9913 / 10000, 99.13%
# [4,  5000] loss: 0.012
# [4, 10000] loss: 0.018
# [4, 15000] loss: 0.015
# [4, 20000] loss: 0.014
# [4, 25000] loss: 0.008
# [4, 30000] loss: 0.020
# [4, 35000] loss: 0.017
# [4, 40000] loss: 0.020
# [4, 45000] loss: 0.014
# [4, 50000] loss: 0.021
# [4, 55000] loss: 0.027
# [4, 60000] loss: 0.025
# 9922 / 10000, 99.22%
# [5,  5000] loss: 0.008
# [5, 10000] loss: 0.018
# [5, 15000] loss: 0.012
# [5, 20000] loss: 0.007