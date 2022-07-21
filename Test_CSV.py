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
        e_class=['family','friend','professional']
        n_class=['child','teenager','adult']
        
        
        N_class=[]
        N_data=self.randomize_node(self.nb_nodes)
        for i in range(self.nb_nodes):
            positionX.append(random.uniform(-100, 100))
            positionY.append(random.uniform(-100, 100))
            N_class.append(random.choice(n_class))
            
            
        U=list(range(self.nb_nodes))
        N_feature=self.randomize_feature(N_class, self.nb_nodes)
        
        df_nodes["id"]=U
        df_nodes['positionX']=positionX
        df_nodes['positionY']=positionY
        df_nodes['class']=N_class
        df_nodes['data']=N_data
        df_nodes['feature']=N_feature
        
        df_nodes.to_csv('../data/TestNodes8.csv',index=False)
        
        source=[]
        E_class=[]
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
                E_class.append(random.choice(e_class))
                M.append(h)


        df_edges["source"]=source
        df_edges['target']=destination
        df_edges['class']=E_class
        df_edges['data']=E_data
        
        df_edges.to_csv('../data/TestLinks8.csv',index=False)
        
        # print(df_edges["source"])
        
        G=nx.MultiGraph()
        
       
        df_nodes = df_nodes.applymap(lambda x: str(x) if type(x)==list else x)
        # print(type(df_nodes["feature"][0]))
        node_attr = df_nodes.set_index('id').to_dict('index')
        G.add_nodes_from(df_nodes["id"])
        nx.set_node_attributes(G, node_attr)
        
        # print(node_attr)
        
        
        L=list(zip(df_edges["source"],df_edges["target"]))
        R=[]
        for i in range(len(L)):
            u=(L[i][0],L[i][1],0)
            while u in R:
                u=(L[i][0],L[i][1],u[2]+1)
            R.append(u)

        G.add_edges_from(R)
        df_edges["ind"]=R
        df_edges.set_index("ind",inplace=True)
        edge_attr = df_edges.to_dict("index")

        nx.set_edge_attributes(G, edge_attr)
        
        # print(G.edges(data=True))
        
        # print(G.nodes(data=True))
        nx.write_gml(G,'../data/Test8.gml')
        
    def randomize_node(self,size):
        
        nom=['henri','madeleine','fabrice','pascale','matthieu','ludivine']
        age=[22,55,34,78,20,65,48]
        
        L=[]
        for i in range(size):
            
            sentence="Name : "+random.choice(nom)+", age : "+str(random.choice(age))
            L.append(sentence)
        return L
        
    def randomize_edge(self,size):
        
        temps=[35,68,97,51,23,68,0,2,3,7,9]
        L=[]
        for i in range(size):
            
            sentence="Knowing since : "+str(random.choice(temps))+" years"
            L.append(sentence)
        return L
    
    def randomize_feature(self,N_class,size):
        L=list(set(N_class))
        M=dict()
        n=len(L)
        
        for i in range(1,n+1):
            M[L[i-1]]=[(100/n)*(i-1),(100/n)*(i)]
        
        feat=[]
        for i in range(size):
            feat.append([random.uniform(M[N_class[i]][0],M[N_class[i]][1]),random.uniform(M[N_class[i]][0],M[N_class[i]][1]),random.uniform(M[N_class[i]][0],M[N_class[i]][1])])
            
        return feat
    


