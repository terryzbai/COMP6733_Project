#!/usr/bin/env python3

import os
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import torch.nn.utils.rnn as rnn_utils
from torch.utils.data import DataLoader

num_epochs = 2
input_dim = 6
output_dim = 6
batch_size = 3
hidden_dim = 4
num_layers = 2
learning_rate = 0.001

def readDataset(dataset_path):
    file_names = os.listdir(dataset_path)
    X = []
    y = []

    for file_name in file_names:
        file_path = os.path.join(dataset_path, file_name)

        series_data = pd.read_csv(file_path, header=None).to_numpy()
        label_data = np.random.rand(series_data.shape[0], hidden_dim)

        X.append(torch.tensor(series_data, dtype=torch.float32))
        y.append(torch.tensor(label_data, dtype=torch.float32))

    return X, y
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

X, y = readDataset('data/')
dataset = Dataset(X, y)
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)
net = nn.LSTM(input_size=input_dim, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True)
criteria = nn.MSELoss()
optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for batch_id, (batch_x, batch_y, batch_x_len) in enumerate(data_loader):
        print(batch_x.size(), batch_y.size(), batch_x_len)
        batch_x_pack = rnn_utils.pack_padded_sequence(batch_x, batch_x_len, batch_first=True)
        out, _ = net(batch_x_pack)
        out_pad, out_len = rnn_utils.pad_packed_sequence(out, batch_first=True)
        print(out_pad.size(), batch_y.size())
        loss = criteria(out_pad, batch_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print('epoch:{:2d}, batch_id:{:2d}, loss:{:6.4f}'.format(epoch, batch_id, loss))
