import sys

import torch
import torch.nn as nn
import torch.optim as optim

import torchvision
import torchvision.transforms as transforms
from torchvision.models import (densenet201, efficientnet_v2_s, mnasnet1_3,
                                mobilenet_v3_large, regnet_y_3_2gf,
                                shufflenet_v2_x2_0)

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

def train():
    nets = {
        'efficientnet_v2_s': efficientnet_v2_s(weights="IMAGENET1K_V1"),
        'regnet_y_3_2gf': regnet_y_3_2gf(weights='IMAGENET1K_V2'),
        'densenet201': densenet201(weights="IMAGENET1K_V1"),
        'mnasnet1_3': mnasnet1_3(weights="IMAGENET1K_V1"),
        'shufflenet_v2_x2_0': shufflenet_v2_x2_0(weights="IMAGENET1K_V1"),
        'mobilenet_v3_large': mobilenet_v3_large(weights='IMAGENET1K_V2')
    }
    for net_name in nets.keys():
        net = nets[net_name].to(device)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

        transform = transforms.Compose([
            transforms.ToTensor(),
        ])

        trainset = torchvision.datasets.ImageFolder('./data/train', transform=transform)

        batch_size = 4

        trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                                shuffle=True, num_workers=2)

        for epoch in range(2):  # loop over the dataset 2 times
            running_loss = 0.0
            for i, data in enumerate(trainloader, 0):
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward + backward + optimize
                outputs = net(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                # print statistics
                running_loss += loss.item()
                if i % 100 == 0:    # print every 100 mini-batches
                    print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
                    running_loss = 0.0

        print('Finished Training')

        torch.save(net, f"{net_name}.pkl")
        print(f"{net_name} saved")

def test():
    net_names = [
        'efficientnet_v2_s', 
        'regnet_y_3_2gf',
        'densenet201',
        'mnasnet1_3',
        'shufflenet_v2_x2_0',
        'mobilenet_v3_large'
    ]

    for net_name in net_names:
        net = torch.load(f'{net_name}.pkl')

        classes = ["malware", "notmalware"]

        transform = transforms.Compose([
            transforms.ToTensor(),
            ])

        valset = torchvision.datasets.ImageFolder('./data/val', transform=transform)

        batch_size = 4

        testloader = torch.utils.data.DataLoader(valset, batch_size=batch_size,
                                                shuffle=True, num_workers=2)

        dataiter = iter(testloader)
        images, labels = dataiter.next()

        correct = 0
        total = 0
        # prepare to count predictions for each class
        correct_pred = {classname: 0 for classname in classes}
        total_pred = {classname: 0 for classname in classes}

        with torch.no_grad():
            for data in testloader:
                images, labels = data
                images = images.to(device)
                labels = labels.to(device)
                
                # calculate outputs by running images through the network
                outputs = net(images)

                # the class with the highest energy is what we choose as prediction
                _, predicted = torch.max(outputs.data, 1)
                _, predictions = torch.max(outputs, 1)
                total += labels.size(0)
                
                correct += (predicted == labels).sum().item()
                
                # collect the correct predictions for each class
                for label, prediction in zip(labels, predictions):
                    if label == prediction:
                        correct_pred[classes[label]] += 1
                    total_pred[classes[label]] += 1

        print(f'Accuracy: {100 * correct // total} %')

        # print accuracy for each class
        for classname, correct_count in correct_pred.items():
            accuracy = 100 * float(correct_count) / total_pred[classname]
            print(f'Accuracy for class: {classname:5s} is {accuracy:.1f} %')
        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please specify train or test")
    elif sys.argv[1] == 'train':
        print("Training")
        train()
    elif sys.argv[1] == 'test':
        print("Testing")
        test()
