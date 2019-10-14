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

model = Net()

import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.0002, momentum=0.9)


from util import train_eval

train_eval(model, criterion, trainloader, testloader, optimizer, epochs=5)
# [1,  5000] loss: 2.293
# [1, 10000] loss: 2.075
# [1, 15000] loss: 1.876
# [1, 20000] loss: 1.754
# [1, 25000] loss: 1.658
# [1, 30000] loss: 1.625
# [1, 35000] loss: 1.558
# [1, 40000] loss: 1.520
# [1, 45000] loss: 1.494
# [1, 50000] loss: 1.459
# 1/5 4456/10000 44.56% (107.18255376815796s)
# [2,  5000] loss: 1.413
# [2, 10000] loss: 1.398
# [2, 15000] loss: 1.386
# [2, 20000] loss: 1.379
# [2, 25000] loss: 1.358
# [2, 30000] loss: 1.324
# [2, 35000] loss: 1.333
# [2, 40000] loss: 1.280
# [2, 45000] loss: 1.296
# [2, 50000] loss: 1.304
# 2/5 5357/10000 53.56999999999999% (105.8866639137268s)
# [3,  5000] loss: 1.226
# [3, 10000] loss: 1.231
# [3, 15000] loss: 1.215
# [3, 20000] loss: 1.235
# [3, 25000] loss: 1.199
# [3, 30000] loss: 1.187
# [3, 35000] loss: 1.192
# [3, 40000] loss: 1.194
# [3, 45000] loss: 1.196
# [3, 50000] loss: 1.191
# 3/5 5729/10000 57.29% (105.63971090316772s)
# [4,  5000] loss: 1.117
# [4, 10000] loss: 1.096
# [4, 15000] loss: 1.121
# [4, 20000] loss: 1.123
# [4, 25000] loss: 1.107
# [4, 30000] loss: 1.120
# [4, 35000] loss: 1.124
# [4, 40000] loss: 1.094
# [4, 45000] loss: 1.105
# [4, 50000] loss: 1.102
# 4/5 5829/10000 58.29% (112.56915497779846s)
# [5,  5000] loss: 1.034
# [5, 10000] loss: 1.024
# [5, 15000] loss: 1.040
# [5, 20000] loss: 1.027
# [5, 25000] loss: 1.043
# [5, 30000] loss: 1.049
# [5, 35000] loss: 1.024
# [5, 40000] loss: 1.042
# [5, 45000] loss: 1.027
# [5, 50000] loss: 1.027
# 5/5 6178/10000 61.78% (109.75669193267822s)
# 61.0% (541.0347754955292s)

