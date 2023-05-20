import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader


def getTrainData(filename='./traindata.txt'):
    data = open(filename, 'r', encoding='utf-8').read()
    train_data = []
    datalist = data.split('\n')
    for vector in datalist:
        vectorlist = vector.split(',')
        train_data.append(vectorlist)
    train_data = np.array(train_data, dtype=float)
    train_x = train_data[:, :-1]
    train_y = train_data[:, -1]
    train_x = torch.tensor(train_x, dtype=torch.float32)
    train_y = torch.tensor(train_y, dtype=torch.float32).reshape(-1, 1)
    train_dataset = torch.utils.data.TensorDataset(train_x, train_y)
    train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)
    return train_loader


def getTestData(filename='./testdata.txt'):
    data = open(filename, 'r', encoding='utf-8').read()
    test_data = []
    datalist = data.split('\n')
    for vector in datalist:
        vectorlist = vector.split(',')
        test_data.append(vectorlist)
    test_data = np.array(test_data, dtype=float)
    test_x = test_data[:, :-1]
    test_y = test_data[:, -1]
    test_x = torch.tensor(test_x, dtype=torch.float32)
    test_y = torch.tensor(test_y, dtype=torch.float32).reshape(-1, 1)
    test_dataset = torch.utils.data.TensorDataset(test_x, test_y)
    test_loader = DataLoader(dataset=test_dataset, batch_size=1404, shuffle=True)
    return test_loader