# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 14:20:43 2022

@author: remit
"""
import dash
from dash.dependencies import Input, Output, State,ALL
from dash import html
import copy
from Stylesheet import Stylesheet
import dash_cytoscape as cyto
import json
# cyto.load_extra_layouts()
import NodeLayout

class CytoView():
    
      
    def __init__(self):
        self.Stylesheet=Stylesheet()
        self.G=[]
        self.G_default=[]
        self.nodeSave=None
        self.edgeSave=None

    def __call__(self,data_nodes,data_edges,CP,stylesheet):
        
        self.data_nodes=data_nodes
        self.data_edges=data_edges
        self.CP=CP
        
        G=[]
        for elem in data_edges:
            if 'class' in elem:
                G.append({
                    'data':{
                    'perso':'e'+str(data_edges.index(elem)),
                    'source': 'n'+str(elem['source']), 
                    'target': 'n'+str(elem['target']),
                    'data': str(elem.get('data'))},
                    'classes': elem['class']
                    })
            else:
                G.append({
                    'data':{
                    'perso':'e'+str(data_edges.index(elem)),
                    'source': 'n'+str(elem['source']), 
                    'target': 'n'+str(elem['target']),
                    'data': str(elem.get('data'))},
                    })
        
        degree=NodeLayout.degree(data_edges,len(data_nodes))
        data_n=NodeLayout.normalisation(data_nodes)
        size=NodeLayout.node_size(degree)
        for elem in data_n:
            if 'class'in elem:
                G.append({
                    'data':{'id': 'n'+str(elem['id']),
                            'label':str((degree[elem['id']],size[elem['id']])),#str((elem['positionX'],elem['positionY'])),
                            'size':size[elem['id']],
                            'borderWidth':size[elem['id']]/10,
                            'data': str(elem.get('data'))
                            },
                    'classes': elem['class'],
                    'position':{'x': 20000*elem['positionX'], 'y': 20000*elem['positionY']},
                    'grabbable': False
                    })
            else :
                G.append({
                    'data':{'id': 'n'+str(elem['id']),
                            'label':str((degree[elem['id']],size[elem['id']])),#str((elem['positionX'],elem['positionY'])),
                            'size':size[elem['id']],
                            'borderWidth':size[elem['id']]/10,
                            'data': str(elem.get('data'))
                            },
                    'position':{'x': 20000*elem['positionX'], 'y': 20000*elem['positionY']},
                    'grabbable': False
                    })
        self.G_default=copy.deepcopy(G)
        self.G=G
        self.Stylesheet.stylesheet_default(stylesheet)
        
    def modif(self):
        #Where G is ordered by default with edges first and nodes second
        CP=self.CP
        
        G=[]
        for i in range(len(CP.mask_edge)):
            if CP.mask_edge[i]:
                G.append(self.G_default[i])
        for j in range(len(CP.mask_node)):
            if CP.mask_node[j]:
                G.append(self.G_default[i+j+1])
        self.G=copy.deepcopy(G)
        
        
        
    def get_callbacks(self,app):

        @app.callback(Output('cytoscape', 'elements'),
        Input('bt-reset-view', 'n_clicks'),
        Input('div-visualization', 'style'),
        Input({"index": ALL,"class": "edge_legend","label":ALL}, "style"),
        Input({"index": ALL,"class": "node_legend","label":ALL}, "style"))
        def reset_layout_view(n_clicks,path,n_style,e_style):
            
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

            if changed_id=='div-visualization':
                return self.G
            elif "legend" in changed_id:
                self.modif()
                return self.G
            else:
                return self.G

        

        @app.callback(Output('cytoscape', 'stylesheet'),
                      Input('cytoscape', 'tapNode'),
                      Input('bt-reset-stylesheet', 'n_clicks'),
                      State('bt-oriented','on'))
        def generate_stylesheet(node,n_clicks,switch):           

            triggered = dash.callback_context.triggered[0]['value']
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

            if 'bt-reset-stylesheet' in changed_id:
                    return self.Stylesheet.default_stylesheet
            else :
                
                if triggered==None:
                    return self.Stylesheet.default_stylesheet
            
                else:
                    self.Stylesheet.stylesheet_on_click(node,switch)
                    return self.Stylesheet.stylesheet
        

        @app.callback(Output('clicked-element', 'children'),
              Input('cytoscape', 'tapNode'),
              Input('cytoscape', 'tapEdge')
              )
        def clicked_element_info(node,edge):
            triggered = dash.callback_context.triggered[0]['value']

            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

            if triggered == None:
                return []
            else :
                if changed_id=='cytoscape.tapEdge' :
                    output=edge["data"]
                else :
                    output=node["data"]
                M=[]
                for elem in output:
                    M.append(html.P(elem+" : " +str(output[elem]),
                                    style={'font-size':'1.6vmin'}))
                return M

            