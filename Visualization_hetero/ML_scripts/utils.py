import pandas as pd 
import numpy as np
import torch 
from torch_geometric.data import HeteroData
import itertools
import copy 


def centr_red(matrix):
    mean = np.zeros(matrix.shape)
    mean_row = matrix.mean(1)

    std = np.zeros(matrix.shape)
    std_row = matrix.std(1)

    for row in range(mean_row.shape[0]):
        mean[row,:] +=  mean_row[row]
        std[row,:] += std_row[row]
    return (matrix-mean)/std


def extract_negative_pairs(entry_data,mts):
    r"""
        Extract all possible negaticve pairs of endry_data of the considered edges that are
        present in mts
        
        Args:
            entry_data(HeteroData): Hetero graph from which we will extract possible negative pairs
            
            mts(Dictionnary): Dictionnary of edge types
        
        Return:
            possible_neg(List): List of tuples of nodes composing the edges
        """
    possible_neg=dict()
    for message_type in mts:
        if "edge_label_index" in entry_data[message_type] : 
            
            #Extraire les liens message_passing :
            mt_T = entry_data[message_type].edge_index
            MP_Us = mt_T[0].tolist()
            MP_Vs = mt_T[1].tolist()
            pos_Us = torch.index_select(entry_data[message_type].edge_label_index[0],
                                         0,torch.where(entry_data[message_type].edge_label==1)[0]).tolist()
            pos_Vs = torch.index_select(entry_data[message_type].edge_label_index[1],
                                         0,torch.where(entry_data[message_type].edge_label==1)[0]).tolist()
            #Liens message passing 
            mt_edges = list(zip(MP_Us, MP_Vs))
            pos_sup_edges = list(zip(pos_Us, pos_Vs))
            possible_U = list(set(MP_Us+pos_Us))
            possible_V = list(set(MP_Vs+pos_Vs))
            all_pairs = list(itertools.product(possible_U, possible_V))
            
            #Extraire les liens negatifs possibles  toutes paires - MP_pairs - supervision_pairs:
            possible_neg[message_type] = list(set(all_pairs)-set(mt_edges)-set(pos_sup_edges))
            
    return possible_neg


def update_negative_sample(entry_data,negative_ratio ,NP):
    r"""
        Each time this function is called take a random sample of a size defined by the negative_ratio
        in the NP set
        
        Args:
            entry_data(HeteroData): Hetero graph from which we will extract possible negative pairs
            
            mts(Dictionnary): Dictionnary of edge types
            
        Return:
            data(HeteroData): Return the HeteroData in which we added the negative pairs to enhance 
            the learning
        """
    data = copy.deepcopy(entry_data)
    neg_pairs = dict()
    
    for message_type in NP:
            
            pos_Us = torch.index_select(data[message_type].edge_label_index[0],
                                         0,torch.where(data[message_type].edge_label==1)[0]).tolist()
            pos_Vs = torch.index_select(data[message_type].edge_label_index[1],
                                         0,torch.where(data[message_type].edge_label==1)[0]).tolist()
            pos_sup_edges = list(zip(pos_Us, pos_Vs))

            choice_idx = np.random.choice(range(len(NP[message_type])),replace=False,
                                                size=int(negative_ratio*len(pos_sup_edges)))
            neg_pairs[message_type] = [NP[message_type][u] for u in choice_idx]
            NE = torch.zeros([2,len(neg_pairs[message_type])],dtype=torch.long)
            NE[0]+=torch.tensor([u for u,v in neg_pairs[message_type]],dtype=torch.long)
            NE[1]+=torch.tensor([v for u,v in neg_pairs[message_type]],dtype=torch.long) 
            PE = torch.stack([torch.tensor(pos_Us,dtype=torch.long),
                                  torch.tensor(pos_Vs,dtype=torch.long)])
            
            setattr(data[message_type],"edge_label_index",torch.cat([PE,NE],dim=1))
            pos_lab = torch.ones(len(pos_Us))
            neg_lab = torch.zeros(NE.size(1))
            setattr(data[message_type],"edge_label",torch.cat([pos_lab,neg_lab], dim=0))
    return data
