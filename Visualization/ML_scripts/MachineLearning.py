# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:22:22 2022

@author: remit
"""


import copy
import pandas as pd
from ML_scripts.my_dataset import MyDataset
from ML_scripts.Train import run
import shutil
import os

data_dir = "../data"

class MachineLearning():
    
    def __init__(self,data_nodes,data_edges):
        self.data_nodes=data_nodes
        self.data_edges=data_edges
        
    def __call__(self):
        self.dataset=MyDataset(self.data_nodes,self.data_edges,data_dir)
        learn = run(self.dataset)
        learn()
        shutil.rmtree(os.path.join('processed',data_dir))
        