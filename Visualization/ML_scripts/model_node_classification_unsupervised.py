# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:45:41 2022

@author: remit
"""

import torch
import torch.nn as nn

import numpy as np
from torch_geometric.nn import GCNConv
from torch.nn.functional import one_hot
from torch.nn import Parameter
from sklearn.linear_model import LogisticRegression


EPS = 1e-15

class Encoder(nn.Module):
    def __init__(self, in_channels, hidden_channels):
        super().__init__()
        self.conv = GCNConv(in_channels, hidden_channels, cached=True)
        self.prelu = nn.PReLU(hidden_channels)

    def forward(self, x, edge_index):
        x = self.conv(x, edge_index)
        x = self.prelu(x)
        return x

class classifier():
    
    def __init__(self,train_z,train_y,test_z,test_y):
        self.trained_classifier = LogisticRegression(solver='lbfgs', multi_class='auto').fit(train_z.detach().cpu().numpy(),train_y.detach().cpu().numpy())
        self.train_z, self.train_y, self.test_z, self.test_y = train_z, train_y, test_z, test_y
    def compute_score(self):
        return self.trained_classifier.score(self.test_z.detach().cpu().numpy(),self.test_y.detach().cpu().numpy())
        
    def predict(self):
        return self.trained_classifier.predict(self.test_z.detach().cpu().numpy())


    
def summary(z,*args,**kwargs):
    return torch.sigmoid(z.mean(dim=0))
    
def train(model,data,optimizer):
    model.train()
    optimizer.zero_grad()
    pos_z, neg_z, summary = model(data.x, data.edge_index)
    loss = model.loss(pos_z, neg_z, summary)
    loss.backward()
    optimizer.step()
    return loss.item()


def corruption(x, edge_index):
    return x[torch.randperm(x.size(0))], edge_index