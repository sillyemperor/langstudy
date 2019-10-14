import torch
import time
import copy


def train_eval(model, criterion, trainloader, testloader, optimizer, lr_scheduler=None, epochs=10, log_count=5000, train_count=0, test_count=0):
    train_time = 0
    max_acc = 0
    best_model_wts = copy.deepcopy(model.state_dict())

    for epoch in range(epochs):  # loop over the dataset multiple times

        model.train()
        running_loss = 0.0
        t = time.time()
        for i, data in enumerate(trainloader, 0):
            if train_count and i > train_count:
                break
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % log_count == (log_count-1):  # print every 2000 mini-batches
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / log_count))
                running_loss = 0.0
        if lr_scheduler:
            lr_scheduler.step()

        t = time.time() - t
        train_time += t

        correct = 0
        total = 0
        model.load_state_dict(best_model_wts)
        model.eval()
        with torch.no_grad():
            for i, data in enumerate(testloader):
                if test_count and i > test_count:
                    break
                images, labels = data
                outputs = model(images)

                _, predicted = torch.max(outputs.data, 1)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        acc = 100 * correct / total
        if acc > max_acc:
            max_acc = acc
            best_model_wts = copy.deepcopy(model.state_dict())

        print(f'{epoch+1}/{epochs} {correct}/{total} {acc}%/{max_acc}% ({t}s)')

    print(f'{100 * max_acc}% ({train_time}s)')
