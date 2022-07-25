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

# from ..inits import reset, uniform

EPS = 1e-15

class DeepGraphInfomax(torch.nn.Module):
    r"""The Deep Graph Infomax model from the
    `"Deep Graph Infomax" <https://arxiv.org/abs/1809.10341>`_
    paper based on user-defined encoder and summary model :math:`\mathcal{E}`
    and :math:`\mathcal{R}` respectively, and a corruption function
    :math:`\mathcal{C}`.

    Args:
        hidden_channels (int): The latent space dimensionality.
        encoder (Module): The encoder module :math:`\mathcal{E}`.
        summary (callable): The readout function :math:`\mathcal{R}`.
        corruption (callable): The corruption function :math:`\mathcal{C}`.
    """
    def __init__(self, hidden_channels, encoder, summary, corruption):
        super(DeepGraphInfomax, self).__init__()
        self.hidden_channels = hidden_channels
        self.encoder = encoder
        self.summary = summary
        self.corruption = corruption

        self.weight = Parameter(torch.Tensor(hidden_channels, hidden_channels))

        # self.reset_parameters()

    # def reset_parameters(self):
    #     reset(self.encoder)
    #     reset(self.summary)
    #     uniform(self.hidden_channels, self.weight)


    def forward(self, *args, **kwargs):
        """Returns the latent space for the input arguments, their
        corruptions and their summary representation."""
        pos_z = self.encoder(*args, **kwargs)
        cor = self.corruption(*args, **kwargs)
        cor = cor if isinstance(cor, tuple) else (cor, )
        neg_z = self.encoder(*cor)
        summary = self.summary(pos_z, *args, **kwargs)
        return pos_z, neg_z, summary


    def discriminate(self, z, summary, sigmoid=True):
        r"""Given the patch-summary pair :obj:`z` and :obj:`summary`, computes
        the probability scores assigned to this patch-summary pair.

        Args:
            z (Tensor): The latent space.
            sigmoid (bool, optional): If set to :obj:`False`, does not apply
                the logistic sigmoid function to the output.
                (default: :obj:`True`)
        """
        value = torch.matmul(z, torch.matmul(self.weight, summary))
        return torch.sigmoid(value) if sigmoid else value


    def loss(self, pos_z, neg_z, summary):
        r"""Computes the mutual information maximization objective."""
        pos_loss = -torch.log(
            self.discriminate(pos_z, summary, sigmoid=True) + EPS).mean()
        neg_loss = -torch.log(1 -
                              self.discriminate(neg_z, summary, sigmoid=True) +
                              EPS).mean()

        return pos_loss + neg_loss


    def test(self, train_z, train_y, test_z, test_y, solver='lbfgs',
             multi_class='auto', *args, **kwargs):
        r"""Evaluates latent space quality via a logistic regression downstream
        task."""
        from sklearn.linear_model import LogisticRegression

        clf = LogisticRegression(solver=solver, multi_class=multi_class, *args,
                                 **kwargs).fit(train_z.detach().cpu().numpy(),
                                               train_y.detach().cpu().numpy())
        return clf.score(test_z.detach().cpu().numpy(),
                         test_y.detach().cpu().numpy()),clf.predict(test_z.detach().cpu().numpy())


    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.hidden_channels)



class Encoder(nn.Module):
    def __init__(self, in_channels, hidden_channels):
        super().__init__()
        self.conv = GCNConv(in_channels, hidden_channels, cached=True)
        self.prelu = nn.PReLU(hidden_channels)

    def forward(self, x, edge_index):
        x = self.conv(x, edge_index)
        x = self.prelu(x)
        return x
    
def summary(z,*args,**kwargs):
    return torch.sigmoid(z.mean(dim=0))
    
def train(model,data,optimizer,device):
    data = data.to(device)
    model.train()
    optimizer.zero_grad()
    pos_z, neg_z, summary = model(data.x, data.edge_index)
    loss = model.loss(pos_z, neg_z, summary)
    loss.backward()
    optimizer.step()
    return loss.item()


def test(model,data,device):
    data = data.to(device)
    model.eval()
    z, _, _ = model(data.x, data.edge_index)
    acc_test,pred = model.test(z[data.train_mask], data.y[data.train_mask],
                     z[data.test_mask], data.y[data.test_mask], max_iter=150)
    # pred=np.eye(np.max(pred)+1)[pred]
    return acc_test,pred
    


def corruption(x, edge_index):
    return x[torch.randperm(x.size(0))], edge_index