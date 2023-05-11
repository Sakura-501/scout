import numpy as np
from sklearn.preprocessing import normalize
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from collections import Counter
import math
import warnings
import numpy as np
import torch.optim
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.model1 = nn.Sequential(
            nn.Conv1d(1, 16, 2),
            nn.ReLU(),
            nn.MaxPool1d(2),  # torch.Size([128, 16, 5])
            nn.Conv1d(16, 32, 2),
            nn.ReLU(),
            nn.MaxPool1d(4),  # torch.Size([128, 32, 1])
            nn.Flatten(),  # torch.Size([128, 32])    (假如上一步的结果为[128, 32, 2]， 那么铺平之后就是[128, 64])
        )
        self.model2 = nn.Sequential(
            nn.Linear(in_features=352, out_features=100),
            nn.Linear(100,20),
            nn.Linear(20,1),
            nn.Sigmoid()
        )

    def forward(self, input):
        input.to(device)
        input = input.reshape(-1,1,98)   #结果为[128,1,11]  目的是把二维变为三维数据
        x = self.model1(input)
        x = self.model2(x)
        return x
# class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
#         self.l1 = nn.Linear(98, 49)
#         self.l2 = nn.Linear(49, 20)
#         self.l3 = nn.Linear(20, 1)
#
#     def forward(self, X_train):
#         X_train = torch.sigmoid(self.l1(X_train))
#         X_train = torch.sigmoid(self.l2(X_train))
#         X_train = torch.sigmoid(self.l3(X_train))
#         return X_train

data=open('./traindata.txt','r',encoding='utf-8').read()
trainData=[]
for vector in data.split('\n')[:-1]:
    trainData.append(vector.split(','))
trainData=trainData[1:]
# print(trainData)
trainData = np.array(trainData)
trainData = normalize(trainData, axis=0, norm='max')
Y_train=trainData[:,-1]
X_train=trainData[:,:-1]

X_train = X_train.astype('float32')
Y_train=Y_train.reshape(-1, 1).astype('float32')
print("shape",Y_train.shape)

# X_train=torch.tensor(X_train)
# Y_train=torch.tensor(Y_train)
encoder = LabelEncoder()
#Y_train = encoder.fit_transform(Y_train.ravel())
X_train, Y_train = torch.FloatTensor(X_train), torch.FloatTensor(Y_train)
train_dataset = torch.utils.data.TensorDataset(X_train, Y_train)

data=open('./testdata.txt','r',encoding='utf-8').read()
testData=[]
for vector in data.split('\n')[:-1]:
    testData.append(vector.split(','))
testData=testData[1:]
# print(testData)
testData = np.array(testData)
testData = normalize(testData, axis=0, norm='max')
Y_test=testData[:,-1]
X_test=testData[:,:-1]
Y_test_dic=Counter(Y_test)
true_goob=Y_test_dic[0.0]
true_bad=Y_test_dic[1.0]
# print(true_bad)
X_test = X_test.astype('float32')
Y_test=Y_test.reshape(-1, 1).astype('float32')
# print(X_test)
# print(Y_test)

X_test=torch.tensor(X_test)
Y_test=torch.tensor(Y_test)
X_test, Y_test = torch.FloatTensor(X_test), torch.FloatTensor(Y_test)
test_dataset = torch.utils.data.TensorDataset(X_test, Y_test)
test_loader = DataLoader(dataset=test_dataset, batch_size=4444, shuffle=True)

# 定义优化器和损失函数
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = Net().to(device)
epochs = 500
learning_rate = 0.001
optimizer = optim.Adam(model.parameters(), learning_rate)
loss_function =nn.BCELoss().to(device)

# optimizer = optim.SGD(model.parameters(), lr=0.8)
# criterion = nn.BCELoss().to(device)

print(X_train)
print("Y_train:\n",Y_train.size())

for i in range(epochs):
    print("--------第{}轮训练开始---------".format(i+1))
    total_G_mean = 0

    train_loader = DataLoader(dataset=train_dataset, batch_size=1696, shuffle=True)
    model.train()
    for data in train_loader:
        X_data, Y_data = data[0], data[1]
        output = model(X_data.to(device))
        loss = loss_function(output, Y_data.to(device))
        print(f'loss: {loss.item()}')
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# for i in range(epochs):
#     print(i)
#     # 读取数据集x,Y_train
#     X_train = X_train.to(device)
#     Y_train = Y_train.to(device)
#     outputs = model(X_train)
#     loss = loss_function(outputs, Y_train).to(device)
#     print(loss.item())
#     optimizer.zero_grad()
#     loss.backward()
#     optimizer.step()

print(f'final loss: {loss.item()}')
data = {
"model_state": model.state_dict(),
}

FILE = "data_sentiment_CNN.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')


Y_res=[]
correct=0
# print(real_evil)
modelres=model(X_test.to(device))
sum=len(modelres)
print("result",modelres)
print("Y_test",Y_test)
for i in range(len(modelres)):
    # print(float(model(X_test)[i]))
    if float(modelres[i])>0.8:
        res=1
    else:
        res=0
    Y_res.append(res)
    if res==Y_test[i]:
        correct=correct+1
print(Y_res)
print(correct)
print(len(modelres))
# input()
print(f"预测正确率：{float(correct)/float(sum)}")

truly_evil_detected=0
real_evil=true_bad
evil_vehicles_reported=Y_res.count(1)
for i in range(len(Y_res)):
    if Y_res[i]==1 and Y_test[i]==1:
        truly_evil_detected+=1

recall=truly_evil_detected/real_evil
print(f"recall:{recall}")
#P
precision=truly_evil_detected/evil_vehicles_reported
print(f"precision:{precision}")
#f1
f1=2*(precision*recall)/(precision+recall)
print(f"f1:{f1}")
