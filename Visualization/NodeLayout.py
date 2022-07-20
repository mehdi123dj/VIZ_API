# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 09:33:19 2022

@author: remit
"""
import numpy as np


def normalisation(data_noeud):
    m = 0
    for elem in data_noeud:
        norm = np.sqrt(elem["positionX"]**2+elem["positionY"]**2)
        if norm > m:
            m = norm

    for elem in data_noeud:
        elem["positionX"] = elem["positionX"]/m
        elem["positionY"] = elem["positionY"]/m
    return data_noeud


def degree(data_edges, L):
    source = []
    target = []
    for elem in data_edges:
        source.append(elem["source"])
        target.append(elem["target"])
    E = list(set(source).union(target))
    degree = {E[i]: 0 for i in range(len(E))}
    for elem in data_edges:
        degree[elem['source']] = degree[elem['source']]+1
        degree[elem['target']] = degree[elem['target']]+1
    return degree


def node_size(degree):

    size = {key: 0 for key in degree.keys()}
    m = 150
    M = 550
    L = np.log(max(degree.values()))
    for key in degree:
        size[key] = (m+np.log(degree[key])/L*(M-m))
    return size
