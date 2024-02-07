import numpy as np
from sklearn.preprocessing import normalize
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.l1 = nn.Linear(98, 49)
        self.l2 = nn.Linear(49, 20)
        self.l3 = nn.Linear(20, 1)

    def forward(self, X_train):
        X_train = torch.sigmoid(self.l1(X_train))
        X_train = torch.sigmoid(self.l2(X_train))
        X_train = torch.sigmoid(self.l3(X_train))
        return X_train

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
print(Y_train)

X_train=torch.tensor(X_train)
Y_train=torch.tensor(Y_train)

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
epoch = 50

model = Net().to(device)
# 定义优化器和损失函数
optimizer = optim.SGD(model.parameters(), lr=0.8)
criterion = nn.BCELoss().to(device)

print(X_train)
print(Y_train)

for i in range(1000):
    print(i)
    # 读取数据集x,Y_train
    X_train = X_train.to(device)
    Y_train = Y_train.to(device)
    outputs = model(X_train)
    loss = criterion(outputs, Y_train).to(device)
    print(loss.item())

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print(f'final loss: {loss.item()}')
data = {
"model_state": model.state_dict(),
}

FILE = "data_sentiment.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
