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
        df_nodes=pd.DataFrame()
        df_edges=pd.DataFrame()
        positionX=[]
        positionY=[]
        e_type=['famille','ami','professionnel','ama','ked','dee','adzd','adaez','asd']
        n_type=['enfant','adolescent','adulte']
        
        
        N_type=[]
        N_data=self.randomize_node(self.nb_nodes)
        for i in range(self.nb_nodes):
            positionX.append(random.uniform(-100, 100))
            positionY.append(random.uniform(-100, 100))
            N_type.append(random.choice(n_type))
            
        U=list(range(self.nb_nodes))
        df_nodes["id"]=U
        df_nodes['positionX']=positionX
        df_nodes['positionY']=positionY
        df_nodes['type']=N_type
        df_nodes['data']=N_data
        
        df_nodes.to_csv('../data/TestNodes5.csv',index=False)
        
        source=[]
        E_type=[]
        destination=[]
        E_data=self.randomize_edge(self.nb_edges)
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
        df_edges['target']=destination
        df_edges['type']=E_type
        df_edges['data']=E_data
        
        df_edges.to_csv('../data/TestLinks5.csv',index=False)
        
        G=nx.MultiGraph()

        for i in range(self.nb_nodes):
            G.add_node(i,positionX=positionX[i],positionY=positionY[i],type=N_type[i],data=N_data[i])
        for i in range(self.nb_edges):
            G.add_edge(source[i],destination[i],type=E_type[i],data=E_data[i])
        nx.write_gml(G,'../data/Test5.gml')
        
    def randomize_node(self,size):
        
        nom=['henri','madeleine','fabrice','pascale','matthieu','ludivine']
        age=[22,55,34,78,20,65,48]
        
        L=[]
        for i in range(size):
            
            sentence="Je m'appelle : "+random.choice(nom)+" et j'ai "+str(random.choice(age))+" ans"
            L.append(sentence)
        return L
        
    def randomize_edge(self,size):
        
        temps=[35,68,97,51,23,68,0,2,3,7,9]
        L=[]
        for i in range(size):
            
            sentence="On se connait depuis : "+str(random.choice(temps))
            L.append(sentence)
        return L