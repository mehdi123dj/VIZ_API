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
        n_color={1:['#339975'],
        2:['#99336d', '#339975'],
        3:['#99336d', '#997533', '#339975'],
        4:['#99336d', '#995533', '#8f9933', '#339975'],
        5:['#99336d', '#993d33', '#997533', '#649933', '#339975'],
        6:['#99336d', '#99333a', '#996433', '#998833', '#449933', '#339975'],
        7:['#99336d', '#993344', '#995533', '#997533', '#8f9933', '#33993a', '#339975'],
        8:['#99336d', '#99334b', '#994733', '#996b33', '#998133', '#799933', '#339949', '#339975']
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
    
    