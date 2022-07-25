# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:22:22 2022

@author: remit
"""


import copy
import pandas as pd
from ML_scripts.my_dataset import MyDataset
from ML_scripts.Train_node_classification_deep import run_node_classif_deep
from ML_scripts.Train_node_classification_unsupervised import run_node_classif_unsupervised
from ML_scripts.Train_edge_prediction_supervised import run_edge_prediction_supervised
from sklearn.manifold import TSNE
import numpy as np
import shutil
import os
import torch
import json

data_dir = "data"
model_dir = "model"

class MachineLearning():
    r"""
    A class that is managing the creation of the pytorch geometric dataset, the training of the model, 
        its registration and return when called a dictionnary of the nodes and their classes
    
    Args:
        
    """
    
    def __init__(self,data_nodes,data_edges,position=False,learn_node_classif_deep=False,learn_edge=False,learn_node_classif_unsupervised=False):
        self.data_nodes=data_nodes
        self.data_edges=data_edges
        self.learn_node_classif_deep=learn_node_classif_deep
        self.learn_edge=learn_edge
        self.learn_node_classif_unsupervised=learn_node_classif_unsupervised
        self.position=position
        
    def __call__(self):
        r"""
            Function that return a dictionnary of the same format then data_nodes after training with new 
            classes attributed compared to the initial data_nodes

        """
        # Creation of the directories in which will be saved the model and the dataset
        os.makedirs(data_dir,exist_ok=True)
        os.makedirs(model_dir,exist_ok=True)

        self.dataset=MyDataset(self.data_nodes,self.data_edges,data_dir)
        
        with open(os.path.join(data_dir,'processed/mapping_class.json'),'r') as f:
            mapping_class = json.load(f)
        with open(os.path.join(data_dir,'processed/mapping_id_node.json'),'r') as f:
            mapping_id_node = json.load(f)
        
        
        mapping_class = {v:u for u,v in mapping_class.items()} 
        
        # Could be used to find back 
        mapping_id_node = {v:u for u,v in mapping_id_node.items()}
        
        df_nodes = pd.DataFrame(self.data_nodes)
        df_edges = pd.DataFrame(self.data_edges)
        
        if self.learn_node_classif_deep :
            learn = run_node_classif_deep(self.dataset)
            
            data_test_nodes = learn()
            data_test_nodes = [mapping_class[elem] for elem in data_test_nodes]
            
            data_test_true_nodes = df_nodes[self.dataset[0].test_mask.tolist()]
            true_class = list(data_test_true_nodes['class'])
            for i in range(len(data_test_true_nodes)):
    
                if true_class[i]!=data_test_nodes[i]:
                    df_nodes.loc[data_test_true_nodes.index[i],'class'] = 'wrong_'+true_class[i]+"_sep_"+data_test_nodes[i]
                else:
                    df_nodes.loc[data_test_true_nodes.index[i],'class'] = 'true_'+data_test_nodes[i]
                    
            if self.position==True:
                
                X_embedded=self.get_embedding(os.path.join(data_dir,'data.pt'),os.path.join(model_dir,os.listdir(model_dir)[0]))
                df_nodes.loc[:,'positionX']=X_embedded[0]
                df_nodes.loc[:,'positionY']=X_embedded[1]
                
            shutil.rmtree(os.path.join(data_dir))
            shutil.rmtree(model_dir)
            return df_nodes.to_dict('records'),self.data_edges
        
        
        elif self.learn_node_classif_unsupervised :
            learn = run_node_classif_unsupervised(self.dataset)
            
            data_test_nodes = learn()
            data_test_nodes = [mapping_class[elem] for elem in data_test_nodes]
            
            data_test_true_nodes = df_nodes[self.dataset[0].test_mask.tolist()]
            true_class = list(data_test_true_nodes['class'])
            for i in range(len(data_test_true_nodes)):
    
                if true_class[i]!=data_test_nodes[i]:
                    df_nodes.loc[data_test_true_nodes.index[i],'class'] = 'wrong_'+true_class[i]+"_sep_"+data_test_nodes[i]
                else:
                    df_nodes.loc[data_test_true_nodes.index[i],'class'] = 'true_'+data_test_nodes[i]
                    
            if self.position==True:
                
                X_embedded=self.get_embedding(os.path.join(data_dir,'data.pt'),os.path.join(model_dir,os.listdir(model_dir)[0]))
                df_nodes.loc[:,'positionX']=X_embedded[0]
                df_nodes.loc[:,'positionY']=X_embedded[1]
                
            shutil.rmtree(os.path.join(data_dir))
            shutil.rmtree(model_dir)
            return df_nodes.to_dict('records'),self.data_edges
        
        else :
            learn = run_edge_prediction_supervised(self.dataset)
            
            data_test_edges = learn()
            source=[]
            target=[]

            
            for i in range(len(data_test_edges[0])):
                source.append(mapping_id_node[data_test_edges[0][i]])
                target.append(mapping_id_node[data_test_edges[1][i]])
            source=pd.Series(source)
            target=pd.Series(target)
            
            df_edges['source']=pd.concat([df_edges['source'], source], ignore_index=True)
            df_edges['target']=pd.concat([df_edges['target'], target], ignore_index=True)
            df_edges['class']=pd.concat([df_edges['class'], pd.Series(['predicted' for elem in data_test_edges[0]])], ignore_index=True)
            # data_test_predicted_edges = [mapping_class[elem] for elem in data_test_nodes]
            print(len(data_test_edges[0]))
            print(data_test_edges)
            
            if self.position==True:
                
                X_embedded=self.get_embedding(os.path.join(data_dir,'data.pt'),os.path.join(model_dir,os.listdir(model_dir)[0]))
                df_nodes.loc[:,'positionX']=X_embedded[0]
                df_nodes.loc[:,'positionY']=X_embedded[1]
            
            shutil.rmtree(os.path.join(data_dir))
            shutil.rmtree(model_dir)
            return df_nodes.to_dict('records'),df_edges.to_dict('records')
            
    
    def get_embedding(self,data_path,model_name):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        Data=self.dataset[0].to(device)
        
        model = torch.load(model_name)
        if 'DeepInfoMax' in model_name:
            Embeddings = model.forward(Data.x,Data.edge_index)[0] # Pb with the forward of deepInfo because return several objects! 
        elif 'edge_pred' in model_name:
            Embeddings = model.encode(Data.x,Data.edge_index)
        else:
            Embeddings = model.forward(Data.x,Data.edge_index)
        Embeddings = Embeddings.detach().cpu().numpy()
        X_embedded = TSNE(n_components=2, learning_rate='auto',
                        init='random').fit_transform(Embeddings)
        X_embedded=X_embedded.transpose()
        return X_embedded


        