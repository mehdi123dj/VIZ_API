# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 13:14:31 2022

@author: remit
"""

import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import pandas as pd
from ControlPanel import ControlPanel
from CytoView import CytoView
from ColorMap import ColorMap
import dash_bootstrap_components as dbc
import dash_daq as daq
import base64
import datetime
import io
from dash import dash_table
import networkx as nx
from networkx.readwrite.gml import literal_destringizer, literal_stringizer
from networkx.exception import NetworkXError
import numpy as np
import copy


keys_nodes=['id','positionX','positionY','class','data','feature']
keys_edges=['source','target','class','data']

def csv_to_df(decoded):

    df = pd.read_csv(io.StringIO(decoded))
    store = register(df)
    return store
    
def gml_to_df(data):

    L = nx.parse_gml(data)
    M=[]
    for elem in L.nodes(data=True):
        g={'id': elem[0]}
        g.update(elem[1])
        M.append(g)
    df_edges = nx.to_pandas_edgelist(L)
    df_nodes = pd.DataFrame.from_records(M)
    df_nodes =df_nodes[df_nodes.columns.intersection(keys_nodes)]

    store_edges = register(df_edges)
    store_nodes = register(df_nodes)
    
    return [store_edges],[store_nodes]
    

# transform df to store dcc object to be registered in the server
def register(df):
    df=copy.deepcopy(df)
    try:
        if 'target' and 'source' in df:
            df=df[df.columns[df.columns.isin(keys_edges)]]
            if "class" in df:
                df["class"] = df["class"].map(str)
            if "data" in df:
                df["data"] = df["data"].map(str)
            df["target"] = df["target"].map(int)
            df["source"] = df["source"].map(int)
            store=dcc.Store(id='stored-data-edges', data=df.to_dict('records'))
            return store
    
        elif 'id' in df :
            if "class" in df.columns:  
                df["class"] = df["class"].map(str)
            if "data" in df.columns:
                df["data"] = df["data"].map(str)
            if "feature" in df.columns:
                df['feature'] = df['feature'].map(lambda x: list(map(float,x.strip("[]").replace("'","").split(","))))
            if "positionX" and "positionY" in df:
                df['positionX'] = df['positionX'].map(float)
                df['positionY'] = df['positionY'].map(float)
            df['id'] = df['id'].map(int)
    
            store=dcc.Store(id='stored-data-nodes', data=df.to_dict('records'))
            return store
        
    except TypeError as e:
        print(e)
        return

    