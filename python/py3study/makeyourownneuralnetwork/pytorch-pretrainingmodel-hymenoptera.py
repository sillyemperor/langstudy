import torch
import torchvision
import torchvision.transforms as transforms
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

transform = transforms.Compose(
    [
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
     ])

root = os.path.join(BASE_DIR, '../data/hymenoptera_data')
trainset = torchvision.datasets.ImageFolder(root=os.path.join(root, 'train'), transform=transform)
trainloader = torch.utils.data.DataLoader(trainset,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.ImageFolder(root=os.path.join(root, 'val'), transform=transform)
testloader = torch.utils.data.DataLoader(testset,
                                         shuffle=False, num_workers=2)


import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler

net = torchvision.models.resnet18(pretrained=True)
for param in net.parameters():
    param.requires_grad = False
num_ftrs = net.fc.in_features
net.fc = nn.Linear(num_ftrs, 2)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
scheduler = lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

for epoch in range(24):  # loop over the dataset multiple times

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
    scheduler.step()

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

# 88 / 153, 57.51633986928105%
# 85 / 153, 55.55555555555556%
# 72 / 153, 47.05882352941177%
# 116 / 153, 75.81699346405229%
# 111 / 153, 72.54901960784314%
# 85 / 153, 55.55555555555556%
# 115 / 153, 75.16339869281046%
# 86 / 153, 56.209150326797385%
# 70 / 153, 45.751633986928105%
# 120 / 153, 78.43137254901961%


