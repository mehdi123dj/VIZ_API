# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:22:22 2022

@author: remit
"""


import copy
import pandas as pd
from ML_scripts.my_dataset import MyDataset
from ML_scripts.Train import run
from ML_scripts.model import AML_model 
from sklearn.manifold import TSNE
import numpy as np
import shutil
import os
import torch
import json

data_dir = "../Visualization/data"
model_dir = "../Visualization/model"

class MachineLearning():
    
    def __init__(self,data_nodes,data_edges,position=False):
        self.data_nodes=data_nodes
        self.data_edges=data_edges
        self.position=position
        
    def __call__(self):

        os.makedirs(data_dir,exist_ok=True)
        os.makedirs(model_dir,exist_ok=True)

        self.dataset=MyDataset(self.data_nodes,self.data_edges,data_dir)
        
        with open(os.path.join(data_dir,'processed/mapping_class.json'),'r') as f:
            mapping_class = json.load(f)
        with open(os.path.join(data_dir,'processed/mapping_id_node.json'),'r') as f:
            mapping_node_id = json.load(f)
        

        mapping_class = {v:u for u,v in mapping_class.items()} 

        learn = run(self.dataset)
        
        data_test_nodes = learn()
        data_test_nodes = [mapping_class[elem] for elem in data_test_nodes]
        

        df_nodes = pd.DataFrame(self.data_nodes)
        data_test_true_nodes = df_nodes[self.dataset[0].test_mask.tolist()]

        for i in range(len(data_test_true_nodes)):

            if list(data_test_true_nodes['class'])[i]!=data_test_nodes[i]:
                df_nodes.loc[data_test_true_nodes.index[i],'class'] = 'wrong_'+data_test_nodes[i]
            else:
                df_nodes.loc[data_test_true_nodes.index[i],'class'] = 'true_'+data_test_nodes[i]
                
        # print(df_nodes['class'])
        # print(os.path.join(data_dir,'data.pt'))
        # print(os.path.join(model_dir,os.listdir(model_dir)[0]))
        if self.position==True:
            
            X_embedded=self.get_embedding(os.path.join(data_dir,'data.pt'),os.path.join(model_dir,os.listdir(model_dir)[0]))
            df_nodes.loc[:,'positionX']=X_embedded[0]
            df_nodes.loc[:,'positionY']=X_embedded[1]
            
        shutil.rmtree(os.path.join(data_dir))
        shutil.rmtree(model_dir)
        return df_nodes.to_dict('records')
    
    def get_embedding(self,data_path,model_name):
        Data=self.dataset[0]
        model = torch.load(model_name)
        Embeddings = model.GNN_model(Data.x,Data.edge_index)
        Embeddings = Embeddings.detach().numpy()
        X_embedded = TSNE(n_components=2, learning_rate='auto',
                        init='random').fit_transform(Embeddings)
        X_embedded=X_embedded.transpose()
        return X_embedded


        