from model import *
from getdata import *
import torch
import torch.optim as optim
import torch.optim
import matplotlib.pyplot as plt
from torch import nn

epochs = 2000
learning_rate = 0.01

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = LSTMClassifier(98, 64).to(device)
optimizer = optim.Adam(model.parameters(), learning_rate)
loss_function = nn.MSELoss()


def train():
    train_loss = []
    for i in range(epochs):
        mean_loss = 0
        print("--------第{}轮训练开始---------".format(i + 1))
        train_loader = getTrainData()
        model.train()
        for data in train_loader:
            x_data, y_data = data[0], data[1]
            x_data = x_data.unsqueeze(1)
            output = model(x_data.to(device))
            loss = loss_function(output, y_data.to(device))
            mean_loss += loss
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        train_loss.append(mean_loss/64)
        print(f'total_loss:{mean_loss}')

    train_loss = [t.cpu().item() for t in train_loss]
    plt.figure()
    plt.plot(list(range(len(train_loss))), train_loss)
    plt.show()

    data = model.state_dict()
    filename = "lstm_model.pth"
    torch.save(data, filename)
    print(f'training complete. file saved to {filename}')



def test():
    test_loader = getTestData()
    for data in test_loader:
        correct = 0
        x_data, y_data = data[0], data[1]
        x_data = x_data.unsqueeze(1)
        model.load_state_dict(torch.load('lstm_model.pth'))
        y_predict = model(x_data.to(device))
        for i in range(len(y_predict)):
            if float(y_predict[i]) > 0.8:
                res = 1
            else:
                res = 0
            if res == y_data[i]:
                correct = correct + 1
        print(f"预测正确率：{float(correct) / float(len(y_data))}")


def main():
    train()
    test()


if __name__ == "__main__":
    main()







