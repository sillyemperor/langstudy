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


import imageio
def isave(name, data):
    print(name, data)
    imageio.imwrite(f'~/tmp/nn/{name}.jpg', data.T)
    return data

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
        isave('inputs', x)
        x = self.conv1(x); isave('1conv1', x)
        x = F.relu(x); isave('1relu', x)
        x = self.pool(x); isave('1pool', x)

        x = self.conv2(x);
        isave('2conv2', x)
        x = F.relu(x);
        isave('2relu', x)
        x = self.pool(x);
        isave('2pool', x)

        # print(x.shape)
        x = x.view(-1, 16 * 5 * 5)
        isave('3view', x)

        # print(x.shape)
        x = self.fc1(x)
        isave('4fc1', x)
        x = F.relu(x)
        isave('4relu', x)
        # print(x.shape)
        x = self.fc2(x)
        isave('5fc2', x)
        x = F.relu(x)
        isave('5relu', x)
        # print(x.shape)
        x = self.fc3(x)
        isave('5fc3', x)
        # print(x.shape)
        return x


model = Net()


inputs, classes = next(iter(testloader))

model(inputs)
