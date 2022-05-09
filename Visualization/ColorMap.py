# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:12:42 2022

@author: remit
"""
import pandas as pd

class ColorMap():
    
    def __init__(self):
        self.edge_legend=[]
        self.stylesheet=[]
        self.node_legend=[]
    
    def __call__(self,data_edges,data_nodes):
        
        
        # Color Map for nodes
        n_color={1:['#a8e3ce'],
        2:['#aa4f82', '#a8e3ce'],
        3:['#aa4f82', '#b79e6f', '#a8e3ce'],
        4:['#aa4f82', '#b5856d', '#b2b690', '#a8e3ce'],
        5:['#aa4f82', '#b37972', '#b79e6f', '#b0c1a0', '#a8e3ce'],
        6:['#aa4f82', '#b17175', '#b78f69', '#b4ac83', '#aec8a9', '#a8e3ce'],
        7:['#aa4f82', '#b06c77', '#b5856d', '#b79e6f', '#b2b690', '#adcdaf', '#a8e3ce'],
        8:['#aa4f82', '#af6878', '#b47e70', '#b89367', '#b5a87e', '#b1bc99', '#acd0b4', '#a8e3ce']
        }
        
        # Color Map for edges
        e_color={1:['#3c005d'],
        2:['#9d9e6f', '#3c005d'],
        3:['#9d9e6f', '#b84e55', '#3c005d'],
        4:['#9d9e6f', '#af695e', '#8f3458', '#3c005d'],
        5:['#9d9e6f', '#ab7662', '#b84e55', '#7a2759', '#3c005d'],
        6:['#9d9e6f', '#a87e65', '#b35e5a', '#9f3e57', '#6e1f5a', '#3c005d'],
        7:['#9d9e6f', '#a68366', '#af695e', '#b84e55', '#8f3458', '#651a5b', '#3c005d'],
        8:['#9d9e6f', '#a58767', '#ac7060', '#b45959', '#a64356', '#832d59', '#5f165b', '#3c005d']
        }
        
        e_type=pd.DataFrame.from_dict(data_edges)
        n_type=pd.DataFrame.from_dict(data_nodes)


        
        type_in_edge="type" in e_type
        type_in_node="type" in n_type

        if type_in_edge==True :
            e_type=list(set(e_type['type']))
            e_type.sort()
            stylesheet=[]
            legend=[]
            m=max(e_color)
            N=len(e_type)
            if N>m:
                c=m
            else:
                c=N
            for i in range(N):
                if i<m:
                    stylesheet.append({
                        'selector': '.'+e_type[i],
                        "style": {
                            "line-color": e_color[c][i]
                        }
                    })
                    legend.append([e_color[c][i],e_type[i]])
                else:
                   legend.append(['#999999',e_type[i]])     
            
            self.edge_legend=legend
            self.stylesheet=self.stylesheet+stylesheet
        
        if type_in_node==True :
            n_type=list(set(n_type['type']))
            n_type.sort()
            stylesheet=[]
            legend=[]
            m=max(n_color)
            N=len(n_type)
            if N>m:
                c=m
            else:
                c=N
            for i in range(N):
                if i<m:
                    stylesheet.append({
                        'selector': '.'+str(n_type[i]),
                        "style": {
                            "color": n_color[c][i],
                            'background-color': n_color[c][i],
                        }
                    })
                    legend.append([n_color[c][i],str(n_type[i])])
                else:
                   legend.append(['#999999',str(n_type[i])])     
            
            
            self.node_legend=legend
            self.stylesheet=self.stylesheet+stylesheet
        
        return self.edge_legend,self.node_legend,self.stylesheet
    
    