# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:22:22 2022

@author: remit
"""


import copy
import pandas as pd
from ML_scripts.my_dataset import MyDataset


data_dir = "./data"

class MachineLearning():
    
    def __init__(self,data_nodes,data_edges):
        self.data_nodes=data_nodes
        self.data_edges=data_edges
        
    def __call__(self):
        self.dataset=MyDataset(self.data_nodes,self.data_edges,data_dir)
        print(self.dataset[0])
        print(self.dataset[0].test_mask)
        print(self.dataset[0].val_mask)
        print(self.dataset[0].train_mask)
        