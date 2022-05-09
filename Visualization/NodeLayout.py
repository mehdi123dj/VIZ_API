# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 09:33:19 2022

@author: remit
"""
import numpy as np
import copy

def normalisation(data_noeud):
    m=0
    for elem in data_noeud:
        norm=np.sqrt(elem["positionX"]**2+elem["positionY"]**2)
        if norm>m:
            m=norm
            
    for elem in data_noeud:
        elem["positionX"]= elem["positionX"]/m
        elem["positionY"]= elem["positionY"]/m
    return data_noeud

def degree(data_edges,L):
    degree=[0 for i in range(L)]
    for elem in data_edges:
        degree[elem['source']]=degree[elem['source']]+1
        degree[elem['destination']]=degree[elem['destination']]+1
    return degree

def node_size(degree):

    size=[]
    m = 10
    M = 500
    L=np.log(max(degree))
    for i in range(len(degree)):
        size.append(m+np.log(degree[i])/L*(M-m))
    return size
    
    
    
    