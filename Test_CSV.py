# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 10:40:48 2022

@author: remit
"""

import pandas as pd
import networkx as nx
import numpy as np
import random

class create_CSV():
    
    def __init__(self,nb_nodes,nb_edges):
        self.nb_nodes=nb_nodes
        self.nb_edges=nb_edges

        
    def create(self):
        df_nodes=pd.DataFrame(columns=['noeuds','positionX','positionY','type'])
        df_edges=pd.DataFrame(columns=['source','type','destination'])
        positionX=[]
        positionY=[]
        e_type=['famille','ami','professionnel','ama','ked','dee','adzd','adaez','asd']
        n_type=['enfant','adolescent','adulte']
        
        
        N_type=[]
        for i in range(self.nb_nodes):
            positionX.append(random.uniform(-100, 100))
            positionY.append(random.uniform(-100, 100))
            N_type.append(random.choice(n_type))
            
        U=list(range(self.nb_nodes))
        df_nodes["noeuds"]=U
        df_nodes['positionX']=positionX
        df_nodes['positionY']=positionY
        df_nodes['type']=N_type
        
        df_nodes.to_csv('../data/csvTestNodes4.csv',index=False)
        
        source=[]
        E_type=[]
        destination=[]

        for i in range(self.nb_edges):
            M=[]
            h=random.sample(U, 2)
            if h in M:
                i=i-1
            else :
                source.append(h[0])
                destination.append(h[1])
                E_type.append(random.choice(e_type))
                M.append(h)

        df_edges["source"]=source
        df_edges['destination']=destination
        df_edges['type']=E_type
        
        df_edges.to_csv('../data/csvTestLinks4.csv',index=False)
    
  