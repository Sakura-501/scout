import numpy as np
from sklearn.preprocessing import normalize
import numpy as np
import torch
import torch.nn as nn

from collections import Counter
import torch.nn.functional as F
import torch.optim as optim

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.l1 = nn.Linear(98, 49)
        self.l2 = nn.Linear(49, 20)
        self.l3 = nn.Linear(20, 1)

    def forward(self, X_test):
        X_test = torch.sigmoid(self.l1(X_test))
        X_test = torch.sigmoid(self.l2(X_test))
        X_test = torch.sigmoid(self.l3(X_test))
        return X_test

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

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

FILE = "data_sentiment.pth"
data = torch.load(FILE)

model_state = data["model_state"]

model = Net().to(device)
model.load_state_dict(model_state)

# print(Y_test)
Y_res=[]
correct=0
# print(real_evil)
modelres=model(X_test.to(device))
sum=len(modelres)
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
