import numpy as np
from sklearn.preprocessing import normalize
import torch
import torch.nn as nn
import torch.optim as optim
from mlp.getData import getData
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

class deepLearn:
    dataGetter = getData()
    def dltrain(self,norPath='',shellPath='',modelFile=''):

        shellData,f,black = self.dataGetter.getWebshellData(shellPath)
        norData,f, white = self.dataGetter.getNormalData(norPath)

        trainData = norData + shellData

        # print(trainData)
        # print(len(trainData))
        trainData = np.array(trainData)
        trainData = normalize(trainData, axis=0, norm='max')
        # print(trainData)
        Y_train = trainData[:, -1]
        X_train = trainData[:, :-1]

        X_train = X_train.astype('float32')
        Y_train = Y_train.reshape(-1, 1).astype('float32')

        # print(X_train)
        # print(Y_train)

        X_train = torch.tensor(X_train)
        Y_train = torch.tensor(Y_train)

        # device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        device = torch.device('cpu')
        epoch = 50

        model = Net().to(device)
        # 定义优化器和损失函数
        optimizer = optim.SGD(model.parameters(), lr=0.8)
        criterion = nn.BCELoss().to(device)

        print(X_train)
        print(Y_train)

        for i in range(20000):
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

        torch.save(data, modelFile)

        print(f'training complete. file saved to {modelFile}')

        return [f'normal files:{white}',f'webshell files:{black}',f'final loss: {loss.item()}',f'training complete. file saved to {modelFile}']


    def dltest(self,filePath='',modelFile='data_sentiment.pth'):
        """
        :param filePath:
        :param modelFile:
        :return: 预测结果 还有文件名列表
        """
        testData,testFile,num=self.dataGetter.getNormalData(filePath)

        testData = np.array(testData)
        testData = normalize(testData, axis=0, norm='max')
        X_test = testData[:, :-1]

        X_test = X_test.astype('float32')

        X_test = torch.tensor(X_test)

        # device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        device = torch.device('cpu')

        FILE = modelFile
        data = torch.load(FILE)

        model_state = data["model_state"]

        model = Net().to(device)
        model.load_state_dict(model_state)

        Y_res = []

        modelres = model(X_test)

        for i in range(len(modelres)):
            # print(float(model(X_test)[i]))
            if float(modelres[i]) > 0.8:
                res = 1
            else:
                res = 0
            Y_res.append(res)
        print(Y_res)
        print(len(modelres))
        return Y_res,testFile
