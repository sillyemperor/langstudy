import torch
import torchvision
import torchvision.transforms as transforms
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

root = os.path.join(BASE_DIR, '../data/')
trainset = torchvision.datasets.CIFAR10(root=root, train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root=root, train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset,
                                         shuffle=False, num_workers=2)

import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # print(x.shape)
        x = self.pool(F.relu(self.conv1(x)))
        # print(x.shape)
        x = self.pool(F.relu(self.conv2(x)))
        # print(x.shape)
        x = x.view(-1, 16 * 5 * 5)
        # print(x.shape)
        x = F.relu(self.fc1(x))
        # print(x.shape)
        x = F.relu(self.fc2(x))
        # print(x.shape)
        x = self.fc3(x)
        # print(x.shape)
        return x
# torch.Size([1, 3, 32, 32])
# torch.Size([1, 6, 14, 14])
# torch.Size([1, 16, 5, 5])
# torch.Size([1, 400])
# torch.Size([1, 120])
# torch.Size([1, 84])
# torch.Size([1, 100])

net = Net()

import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.0002, momentum=0.9)

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

    print(f'{epoch} {correct} / {total}, {100 * correct / total}%')
#
# [1,  5000] loss: 2.294
# [1, 10000] loss: 2.138
# [1, 15000] loss: 1.931
# [1, 20000] loss: 1.786
# [1, 25000] loss: 1.695
# [1, 30000] loss: 1.611
# [1, 35000] loss: 1.557
# [1, 40000] loss: 1.525
# [1, 45000] loss: 1.490
# [1, 50000] loss: 1.446
# 0 4973 / 10000, 49.73%
# [2,  5000] loss: 1.433
# [2, 10000] loss: 1.358
# [2, 15000] loss: 1.384
# [2, 20000] loss: 1.329
# [2, 25000] loss: 1.350
# [2, 30000] loss: 1.346
# [2, 35000] loss: 1.287
# [2, 40000] loss: 1.304
# [2, 45000] loss: 1.289
# [2, 50000] loss: 1.284
# 1 5607 / 10000, 56.07%
# [3,  5000] loss: 1.214
# [3, 10000] loss: 1.216
# [3, 15000] loss: 1.200
# [3, 20000] loss: 1.198
# [3, 25000] loss: 1.217
# [3, 30000] loss: 1.192
# [3, 35000] loss: 1.207
# [3, 40000] loss: 1.179
# [3, 45000] loss: 1.173
# [3, 50000] loss: 1.206
# 2 5743 / 10000, 57.43%
# [4,  5000] loss: 1.118
# [4, 10000] loss: 1.117
# [4, 15000] loss: 1.069
# [4, 20000] loss: 1.106
# [4, 25000] loss: 1.088
# [4, 30000] loss: 1.143
# [4, 35000] loss: 1.088
# [4, 40000] loss: 1.082
# [4, 45000] loss: 1.105
# [4, 50000] loss: 1.110
# 3 5933 / 10000, 59.33%
# [5,  5000] loss: 1.011
# [5, 10000] loss: 1.044
# [5, 15000] loss: 1.039
# [5, 20000] loss: 1.042
# [5, 25000] loss: 1.038
# [5, 30000] loss: 1.024
# [5, 35000] loss: 1.047
# [5, 40000] loss: 1.029
# [5, 45000] loss: 1.056
# [5, 50000] loss: 1.007
# 4 6106 / 10000, 61.06%
# [6,  5000] loss: 0.939
# [6, 10000] loss: 0.956
# [6, 15000] loss: 0.983
# [6, 20000] loss: 0.957
# [6, 25000] loss: 0.962
# [6, 30000] loss: 0.972
# [6, 35000] loss: 0.973
# [6, 40000] loss: 1.016
# [6, 45000] loss: 0.965
# [6, 50000] loss: 1.011
# 5 6255 / 10000, 62.55%
# [7,  5000] loss: 0.868
# [7, 10000] loss: 0.907
# [7, 15000] loss: 0.923
# [7, 20000] loss: 0.912
# [7, 25000] loss: 0.931
# [7, 30000] loss: 0.923
# [7, 35000] loss: 0.945
# [7, 40000] loss: 0.951
# [7, 45000] loss: 0.937
# [7, 50000] loss: 0.940
# 6 6225 / 10000, 62.25%
# [8,  5000] loss: 0.837
# [8, 10000] loss: 0.866
# [8, 15000] loss: 0.871
# [8, 20000] loss: 0.853
# [8, 25000] loss: 0.875
# [8, 30000] loss: 0.891
# [8, 35000] loss: 0.918
# [8, 40000] loss: 0.894
# [8, 45000] loss: 0.915
# [8, 50000] loss: 0.905
# 7 6268 / 10000, 62.68%
# [9,  5000] loss: 0.775
# [9, 10000] loss: 0.798
# [9, 15000] loss: 0.829
# [9, 20000] loss: 0.842
# [9, 25000] loss: 0.854
# [9, 30000] loss: 0.859
# [9, 35000] loss: 0.855
# [9, 40000] loss: 0.903
# [9, 45000] loss: 0.858
# [9, 50000] loss: 0.883
# 8 6349 / 10000, 63.49%
# [10,  5000] loss: 0.741
# [10, 10000] loss: 0.761
# [10, 15000] loss: 0.810
# [10, 20000] loss: 0.804
# [10, 25000] loss: 0.810
# [10, 30000] loss: 0.808
# [10, 35000] loss: 0.803
# [10, 40000] loss: 0.829
# [10, 45000] loss: 0.855
# [10, 50000] loss: 0.854
# 9 6306 / 10000, 63.06%

