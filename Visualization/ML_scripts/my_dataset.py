# -*- coding: utf-8 -*-

import os
from typing import Callable, List, Optional
import torch
from torch_geometric.data import Data,InMemoryDataset,download_url, extract_zip
import pandas as pd
import random
import json

import numpy as np

class MyDataset(InMemoryDataset):
    
    def __init__(
                self,
                data_nodes,
                data_edges,
                root: str, 
                transform: Optional[Callable] = None,
                pre_transform: Optional[Callable] = None,
                ):
        
        self.data_nodes=data_nodes
        self.data_edges=data_edges
        super().__init__(root, transform, pre_transform)
        self.data,self.slices = torch.load(self.processed_paths[0])
        

            
    # @property
    # def raw_file_names(self) -> List[str]:
    #     return [
    #         'elliptic_txs_features.csv',
    #         'elliptic_txs_edgelist.csv',
    #         'elliptic_txs_classes.csv',
    #     ]
    
    @property
    def processed_file_names(self) -> str:
        return ['data.pt','mapping.json']

    def process(self):
        # print(self.data_nodes)
        df_nodes = pd.DataFrame(self.data_nodes)
        df_features = df_nodes["feature"]
        
        df_edges = pd.DataFrame(self.data_edges)[['source','target']]
        
        df_classes = df_nodes["class"]
        mapping={}
        cnt=0
        for elem in df_classes.unique():
            mapping[elem] = cnt
            cnt+=1
        
        
        index = df_nodes.index
        n=len(index)

        
        # dividing the set into 3 parts : train,val,test 

        
        index = set(index)
        train = set(random.sample(list(index),round(n*0.8)))
        val = set(random.sample(list(index - train),round(n*0.1)))
        test = index - train - val
        # Parts=[train,val,test]
        
        
        node_features = torch.tensor(df_features)
        edge_index = torch.transpose(torch.tensor(list(zip(df_edges["source"],df_edges["target"]))).long(),1,0)
        train_mask = torch.tensor(df_nodes.index.isin(list(train)))
        val_mask = torch.tensor(df_nodes.index.isin(list(val)))
        test_mask = torch.tensor(df_nodes.index.isin(list(test)))
        y = torch.tensor(df_classes.map(mapping))

            
        data = Data(x = node_features,
                    edge_index = edge_index,
                    y = y,
                    )
        

        train_mask,val_mask,test_mask=torch.tensor([False]*n),torch.tensor([False]*n),torch.tensor([False]*n)
        
        
        for c in range(len(mapping)):
            idx = (data.y == c).nonzero(as_tuple=False).view(-1)
            idx = idx[torch.randperm(idx.size(0))[:round(len(df_nodes.groupby('class').groups[list(mapping.keys())[c]])*0.8)]]
            print(idx)
            train_mask[idx] = True
    
        remaining = (~train_mask).nonzero(as_tuple=False).view(-1)
        remaining = remaining[torch.randperm(remaining.size(0))]
    
    
        num_val=round(n*0.1)

        # data.val_mask.fill_(False)
        val_mask[remaining[:num_val]] = True
    
        # data.test_mask.fill_(False)
        test_mask[remaining[num_val:]] = True
    
        data.train_mask = train_mask
        data.val_mask = val_mask
        data.test_mask = test_mask
        
        
        data = data if self.pre_transform is None else self.pre_transform(data)
        torch.save(self.collate([data]), self.processed_paths[0])

        with open(self.processed_paths[1], 'w') as f:
            json.dump(mapping, f)
            

    # @property
    # def num_classes(self) -> int:
    #     n=len(set(self.data.y))
    #     # df_nodes = pd.DataFrame(self.data_nodes)
    #     # n = len(list(df_nodes['class']).unique())
    #     print("Number of classes: ",n)
    #     return n
    
    # @property
    # def num_features(self) -> int:
    #     # df_nodes = pd.DataFrame(self.data_nodes)
    #     n = len(self.data.x[0])
    #     print("Number of feature: ",n)
    #     return n

