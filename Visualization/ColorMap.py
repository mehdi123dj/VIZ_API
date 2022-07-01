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
    
    def __call__(self,data_edges,data_nodes,classif=False):
        
        
        # Color Map for nodes
        n_color={1:['#339975'],
        # 2:['#85b307', '#e96060'],
        2:['#99336d', '#339975'],
        # 3:['#85b307', '#e96060', '#999999'],
        3:['#99336d', '#997533', '#339975'],
        4:['#99336d', '#995533', '#8f9933', '#339975'],
        5:['#99336d', '#993d33', '#997533', '#649933', '#339975'],
        6:['#99336d', '#99333a', '#996433', '#998833', '#449933', '#339975'],
        7:['#99336d', '#993344', '#995533', '#997533', '#8f9933', '#33993a', '#339975'],
        8:['#99336d', '#99334b', '#994733', '#996b33', '#998133', '#799933', '#339949', '#339975']
        }
        

        
        if classif==False:

            df_node=pd.DataFrame.from_dict(data_nodes)
            
            stylesheet=[]
            legend=[]
            self.edge_stylesheet_legend(data_edges)
            
            if 'class' in df_node:
                n_class=list(set(df_node['class']))
                n_class.sort()
    
                m=max(n_color)
                N=len(n_class)
                if N>m:
                    c=m
                else:
                    c=N
                for i in range(N):
                    if i<m and n_class[i]!='nan':
                        stylesheet.append({
                            'selector': '.'+str(n_class[i]),
                            "style": {
                                "color": n_color[c][i],
                                'background-color': n_color[c][i],
                            }
                        })
                        legend.append([n_color[c][i],str(n_class[i])])
                    else:
                        legend.append(['#999999',str(n_class[i])])     
            

            self.node_legend=legend
            self.stylesheet=self.stylesheet+stylesheet
        
        else :
            
            df_node=pd.DataFrame.from_dict(data_nodes)

            self.edge_stylesheet_legend(data_edges)

            n_class=list(set(df_node['class']))
            n_real_class=[elem for elem in n_class if "wrong" not in elem and "true" not in elem]
            n_predicted_class=[elem for elem in n_class if "wrong" in elem or "true" in elem]
            n_real_class.sort()
            stylesheet=[]
            legend=[]
            m=max(n_color)
            N=len(n_real_class)
            if N>m:
                c=m
            else:
                c=N
                
            for i in range(N):
                if i<m and n_class[i]!='nan':
                    stylesheet.append({
                        'selector': '.'+str(n_real_class[i]),
                        "style": {
                            "color": n_color[c][i],
                            'background-color': n_color[c][i],
                        }
                    })
                    legend.append([n_color[c][i],str(n_real_class[i])])
                else:
                    legend.append(['#999999',str(n_real_class[i])])
                    
            for j in range(len(n_predicted_class)):
                if "wrong" in n_predicted_class[j] and n_predicted_class[j]!='nan':

                    real_class, wrong_class = n_predicted_class[j].split("wrong_")[1].split('_sep_')
                    # print(real_class)
                    # print(wrong_class)

                    index_real = n_real_class.index(real_class)
                    index_wrong = n_real_class.index(wrong_class)
                    # print(n_color[c][index_wrong])
                    stylesheet.append({
                        'selector': '.'+str(n_predicted_class[j]),
                        "style": {
                            'border-color': n_color[c][index_wrong],
                            'border-width': 'data(borderWidth)',
                            'background-color': n_color[c][index_real],
                        }
                    })
                    legend.append([n_color[c][index_real],str(n_predicted_class[j])])
                elif "true" in n_predicted_class[j] and n_predicted_class[j]!='nan':
                    index = n_real_class.index(n_predicted_class[j].split("true_")[1])
                    stylesheet.append({
                        'selector': '.'+str(n_predicted_class[j]),
                        "style": {
                            'border-color': "#00FF00",
                            'border-width': 'data(borderWidth)',
                            'background-color': n_color[c][index],
                        }
                    })
                    legend.append([n_color[c][index],str(n_predicted_class[j])])
                else:
                    legend.append(['#999999',str(n_predicted_class[j])])     
            
            
            self.node_legend=legend
            self.stylesheet=self.stylesheet+stylesheet
        return self.edge_legend,self.node_legend,self.stylesheet
    
    def edge_stylesheet_legend(self,data_edges):
        
        # Color Map for edges
        e_color={1:['#000000'],
        2:['#9d9e6f', '#3c005d'],
        3:['#9d9e6f', '#b84e55', '#3c005d'],
        4:['#9d9e6f', '#af695e', '#8f3458', '#3c005d'],
        5:['#9d9e6f', '#ab7662', '#b84e55', '#7a2759', '#3c005d'],
        6:['#9d9e6f', '#a87e65', '#b35e5a', '#9f3e57', '#6e1f5a', '#3c005d'],
        7:['#9d9e6f', '#a68366', '#af695e', '#b84e55', '#8f3458', '#651a5b', '#3c005d'],
        8:['#9d9e6f', '#a58767', '#ac7060', '#b45959', '#a64356', '#832d59', '#5f165b', '#3c005d']
        }
        
        e_class=pd.DataFrame.from_dict(data_edges)
        class_in_edge="class" in e_class
        if class_in_edge==True :
            e_class=list(set(e_class['class']))
            e_class.sort()
            stylesheet=[]
            legend=[]
            m=max(e_color)
            N=len(e_class)
            if N>m:
                c=m
            else:
                c=N
            for i in range(N):
                if i<m and e_class[i]!='nan':
                    stylesheet.append({
                        'selector': '.'+e_class[i],
                        "style": {
                            "line-color": e_color[c][i]
                        }
                    })
                    legend.append([e_color[c][i],e_class[i]])
                else:
                   legend.append(['#999999',e_class[i]])     
            
            self.edge_legend=legend
            self.stylesheet=self.stylesheet+stylesheet