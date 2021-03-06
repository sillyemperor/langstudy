#!/usr/bin/env python
# coding: utf-8

# In[2]:


import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy

plt.ion()   # interactive mode


# In[3]:


# Data augmentation and normalization for training
# Just normalization for validation
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

data_dir = '../data/pets'
image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                          data_transforms[x])
                  for x in ['train', 'val']}

dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=4,
                                             shuffle=True, num_workers=0)
              for x in ['train', 'val']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
class_names = image_datasets['train'].classes

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def train_model(model, criterion, optimizer, scheduler, num_epochs=25):
    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            data_count = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                data_count += 1
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
            if phase == 'train':
                scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, best_acc


def run_benchmark(name, model_ft, num_epochs=10):
    print(f'-------------------{name}-------------------')
    for param in model_ft.parameters():
        param.requires_grad = False

    num_ftrs = model_ft.fc.in_features
    # Here the size of each output sample is set to 2.
    # Alternatively, it can be generalized to nn.Linear(num_ftrs, len(class_names)).
    model_ft.fc = nn.Linear(num_ftrs, len(class_names))

    model_ft = model_ft.to(device)

    criterion = nn.CrossEntropyLoss()

    # Observe that all parameters are being optimized
    optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)

    # Decay LR by a factor of 0.1 every 7 epochs
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

    model_ft, best_acc = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler,
                                     num_epochs=num_epochs)
    print(best_acc)
    print()


run_benchmark('ResNet18', models.resnet18(pretrained=True))
run_benchmark('ResNet34', models.resnet34(pretrained=True))
run_benchmark('ResNet50', models.resnet50(pretrained=True))
run_benchmark('ResNet101', models.resnet101(pretrained=True))
run_benchmark('ResNet152', models.resnet152(pretrained=True))

# num_epochs=5
# -------------------ResNet18-------------------
#
# Training complete in 5m 16s
# Best val Acc: 0.937107
# tensor(0.9371, dtype=torch.float64)
#
# -------------------ResNet34-------------------
#
# Training complete in 8m 36s
# Best val Acc: 0.924528
# tensor(0.9245, dtype=torch.float64)
#
# -------------------ResNet50-------------------
#
# Training complete in 15m 52s
# Best val Acc: 0.949686
# tensor(0.9497, dtype=torch.float64)
#
# -------------------ResNet101-------------------
#
# Training complete in 24m 10s
# Best val Acc: 0.930818
# tensor(0.9308, dtype=torch.float64)
#
# -------------------ResNet152-------------------
#
# Training complete in 34m 5s
# Best val Acc: 0.962264
# tensor(0.9623, dtype=torch.float64)

#num_epochs=10
# -------------------ResNet18-------------------
# Training complete in 11m 25s
# Best val Acc: 0.937107
# tensor(0.9371, dtype=torch.float64)
#
# -------------------ResNet34-------------------
#
# Training complete in 19m 10s
# Best val Acc: 0.962264
# tensor(0.9623, dtype=torch.float64)
#
# -------------------ResNet50-------------------
#
# Training complete in 32m 13s
# Best val Acc: 0.955975
# tensor(0.9560, dtype=torch.float64)
#
# -------------------ResNet101-------------------
#
# Training complete in 49m 11s
# Best val Acc: 0.937107
# tensor(0.9371, dtype=torch.float64)
#
# -------------------ResNet152-------------------
#
# Training complete in 69m 13s
# Best val Acc: 0.968553
# tensor(0.9686, dtype=torch.float64)
