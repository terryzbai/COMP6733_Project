#!/usr/bin/env python3

import os
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch.nn.utils.rnn as rnn_utils
from torch.utils.data import DataLoader

dataset_path = 'data_stml/'
num_epochs = 50
input_dim = 6
output_dim = 6
batch_size = 3
hidden_dim = 4
num_layers = 2
learning_rate = 0.001

def predFloatToLabel(pred):
    return 1.0 if pred > 0 else 0.0


def readDataset(dataset_path):
    file_names = os.listdir(dataset_path)
    X = []
    y = []

    for file_name in file_names:
        file_path = os.path.join(dataset_path, file_name)

        data = pd.read_csv(file_path, header=None).to_numpy()
        series_data = data[:, :6]
        # label_data = np.random.rand(series_data.shape[0], hidden_dim)
        label_data = data[:, -4:]

        X.append(torch.tensor(series_data, dtype=torch.float32))
        y.append(torch.tensor(label_data, dtype=torch.float32))

    return X, y, file_names

class Dataset(torch.utils.data.Dataset):
    def __init__(self, data, label):
        self.data = data
        self.label = label

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        tuple_ = (self.data[idx], self.label[idx])
        return tuple_


def collate_fn(data_tuple):   # data_tuple是一个列表，列表中包含batchsize个元组，每个元组中包含数据和标签
    data_tuple.sort(key=lambda x: len(x[0]), reverse=True)
    data = [sq[0] for sq in data_tuple]
    label = [sq[1] for sq in data_tuple]
    data_length = [len(sq) for sq in data]
    data = rnn_utils.pad_sequence(data, batch_first=True, padding_value=0.0)     # 用零补充，使长度对齐
    label = rnn_utils.pad_sequence(label, batch_first=True, padding_value=0.0)   # 这行代码只是为了把列表变为tensor
    return data, label, data_length

X, y, file_names = readDataset(dataset_path)
dataset = Dataset(X, y)
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)
net = nn.LSTM(input_size=input_dim, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True)
criteria = nn.MSELoss()
optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for batch_id, (batch_x, batch_y, batch_x_len) in enumerate(data_loader):
        batch_x_pack = rnn_utils.pack_padded_sequence(batch_x, batch_x_len, batch_first=True)
        out, _ = net(batch_x_pack)
        out_pad, out_len = rnn_utils.pad_packed_sequence(out, batch_first=True)
        batch_y_pred = out_pad.detach().cpu().numpy()
        batch_y_true = batch_y.detach().cpu().numpy()
        loss = criteria(out_pad, batch_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print('epoch:{:2d}, batch_id:{:2d}, loss:{:6.4f}'.format(epoch, batch_id, loss))



print("-------------------")
for batch_id, (batch_x, batch_y, batch_x_len) in enumerate(data_loader):
    batch_x_pack = rnn_utils.pack_padded_sequence(batch_x, batch_x_len, batch_first=True)
    out, _ = net(batch_x_pack)
    out_pad, out_len = rnn_utils.pad_packed_sequence(out, batch_first=True)
    batch_y_pred = out_pad.detach().cpu().numpy()[:, :, -1]
    batch_y_true = batch_y.detach().cpu().numpy()[:, :, -1]
    print(batch_y_true.shape)
    sample_idx = 0
    for series_pred, series_true  in zip(batch_y_pred, batch_y_true):
        print("---" * 10)
        file_name = file_names[batch_id * batch_size + sample_idx]
        file_path = os.path.join(dataset_path, file_name)
        print(file_path)

        cut_pred = []
        cut_true = []
        for index, (pred, true) in enumerate(zip(series_pred, series_true)):
            pred_label = predFloatToLabel(pred)
            if index > 0 and pred_label != predFloatToLabel(series_pred[index-1]):
                cut_pred.append(index)
            if index > 0 and true != series_true[index-1]:
                cut_true.append(index)

            # print("pred: {}, pred_label: {}, true_label: {}".format(pred, pred_label, true))

        sample_idx += 1
        data = pd.read_csv(file_path, header=None).to_numpy()
        print(data.shape)


        plt.figure(figsize=(15, 8))
        # Plot for the first column
        plt.subplot(2, 1, 1)
        plt.plot(range(0,data.shape[0]*10,10), data[:, 0], color='r')
        plt.plot(range(0,data.shape[0]*10,10), data[:, 1], color='g')
        plt.plot(range(0,data.shape[0]*10,10), data[:, 2], color='b')

        for i in range(len(cut_true)):
            plt.axvline(x=cut_true[i]*10, color='r', linestyle='--')
            # plt.axvline(x=cut_true[i][-1]*10, color='g', linestyle='--')

        plt.title('Accelerometer - Ground Truth Cut', fontsize=24)
        plt.xlabel('Time(ms)', fontsize=24)
        plt.ylabel('Value(g)', fontsize=24)
        plt.ylim(-5, 5)
        plt.legend()

        # Plot for the second column
        plt.subplot(2, 1, 2)
        plt.plot(range(0,data.shape[0]*10,10), data[:, 0], color='r')
        plt.plot(range(0,data.shape[0]*10,10), data[:, 1], color='g')
        plt.plot(range(0,data.shape[0]*10,10), data[:, 2], color='b')

        for i in range(len(cut_pred)):
            plt.axvline(x=cut_pred[i]*10, color='r', linestyle='--')

        plt.title('Accelerameter - LSTM Cut', fontsize=24)
        plt.xlabel('Time(ms)', fontsize=24)
        plt.ylabel('Value(g)', fontsize=24)
        plt.ylim(-5, 5)
        plt.legend()

        plt.tight_layout()
        plt.show()

        break
    break
