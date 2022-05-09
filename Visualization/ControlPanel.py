# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 11:01:11 2022

@author: remit
"""
import json
import dash
import copy
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State, MATCH, ALL


class ControlPanel():
    def __init__(self):
        self.styles={
            'tab': {
                'height': '77vh',
                'maxHeight': '77vh',
                'overflow-y': 'scroll',
                'background-color':'#c7c7c7',
                'padding':'2%'
            }
        }


    def __call__(self,edge_legend,node_legend,data_edges,data_nodes):

        self.hash_node={}
        for elem in node_legend:
            self.hash_node[elem[1]]={"selected":1,"data":[]}
        if self.hash_node!={}:
            for elem in data_nodes:
                self.hash_node[elem["type"]]["data"]=self.hash_node[elem["type"]]["data"]+[elem["noeuds"]]

        
        self.hash_edge={}
        for elem in edge_legend:
            self.hash_edge[elem[1]]={"selected":1,"data":[]}
        if self.hash_edge!={}:
            c=0
            for elem in data_edges:
                self.hash_edge[elem["type"]]["data"]=self.hash_edge[elem["type"]]["data"]+[c]
                c+=1

        
        self.mask_edge=[1 for elem in data_edges]
        self.mask_node=[1 for elem in data_nodes]
        
        self.E=[html.Div(id={'type':'edge_legend','index': edge_legend.index(elem),'label':elem[1]},
            children=[
            html.Div([html.P(elem[1],style={'text-overflow': 'ellipsis'})],
                     style={'width':'59%','height':'2em','display':'inline-flex','align-items': 'center','justify-content': 'center'}),
            html.Div(style={'width':'40%','height':'2em','display':'inline-block','background-color':elem[0]})
            ]) for elem in edge_legend]
        
        self.N=[html.Div(id={'type':'node_legend','index': node_legend.index(elem),'label':elem[1]},
            children=[
            html.Div([html.P(elem[1],style={'text-overflow': 'ellipsis'})],
                     style={'width':'59%','height':'2em','display':'inline-flex','align-items': 'center','justify-content': 'center'}),
            html.Div(style={'width':'40%','height':'2em','display':'inline-block','background-color':elem[0]})
            ]) for elem in node_legend]

    def create_CP(self):
        return html.Div([
                dcc.Tabs(id='tabs', children=[
                    dcc.Tab(label='Legend', children=[
                        html.Div([
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.B(children='Nodes Legend'),
                                            html.Div(id='nodes-legend',
                                                     children=self.N,
                                            )
                                        ]
                                    )
                                    
                                ],style={'background-color':'#F0F0F0','padding':'3%','margin':'4%'}
                            ),
                            
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.B(children='Edges legend'),
                                            html.Div(id='edges-legend',
                                                children=self.E,

                                            )
                                        ]
                                    )
                                    
                                ],style={'background-color':'#F0F0F0','padding':'3%','margin':'4%'}
                                    
                            ),
                            
                            
                            html.Div(
                                children=[
                                    html.B(children='Clicked element'),
                                    html.Div(id='clicked-element',
                                        children=[]
                                        )
                                ],style={'background-color':'#F0F0F0','padding':'3%','margin':'4%'}
                            ),
                        ],style=self.styles['tab'])

                        

                    ]),
            
                    dcc.Tab(label='Export', children=[
                        html.Div(style=self.styles['tab'], children=[
                            html.Button("as jpg", id="btn-get-jpg"),
                            html.Button("as png", id="btn-get-png"),
                            html.Button("as svg", id="btn-get-svg")]
                            )
                        ])
                    ]),
                    
                    
                ],style={'width': '20%','display':'inline-block', 'verticalAlign': 'top'})
    
    
    
    def get_callbacks(self,app):    
        
        @app.callback(
            Output("cytoscape", "generateImage"),
            [
                Input("btn-get-jpg", "n_clicks"),
                Input("btn-get-png", "n_clicks"),
                Input("btn-get-svg", "n_clicks"),
            ])
        def get_image( get_jpg_clicks, get_png_clicks, get_svg_clicks):
        
            
    
            # 'store': Stores the image data in 'imageData' !only jpg/png are supported
            # 'download'`: Downloads the image as a file with all data handling
            # 'both'`: Stores image data and downloads image as file.
            action = 'store'
            ftype=None
            ctx = dash.callback_context
            if ctx.triggered:
                input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
                # File type to output of 'svg, 'png', 'jpg', or 'jpeg' (alias of 'jpg')
                ftype = input_id
                if input_id != "tabs":
                    action = "download"
                    ftype = input_id.split("-")[-1]
        
            return {
                'type': ftype,
                'action': action
                }
        
        
        
        #TODO : If we click rapidly on multiple links callbacks will be fired before the 
        # one before had finished
        @app.callback(
            Output({"index": MATCH,"type": "edge_legend","label":MATCH}, "style"),
            Input({"index": MATCH,"type": "edge_legend","label":MATCH}, "n_clicks"),
            State('stored-data-edges','data'),
        )
        def edge_selection(n,data_edge):
            triggered = dash.callback_context.triggered
            
            if n is None :
                return {'height':'5vh','margin':"2%",'display':'flex','align-items': 'center'}
            
            elif n % 2 == 0:
                new_mask_edge=self.mask_edge
                for i in self.hash_edge[json.loads(triggered[0]['prop_id'].split('.')[0])["label"]]["data"]:
                    if self.mask_node[data_edge[i]['source']]==1 and self.mask_node[data_edge[i]['destination']]==1:
                        new_mask_edge[i]=1
                self.hash_edge[json.loads(triggered[0]['prop_id'].split('.')[0])["label"]]["selected"]=1
                self.mask_edge=copy.deepcopy(new_mask_edge)
                return {'height':'5vh','margin':"2%",'display':'flex','align-items': 'center'}
            
            else:
                new_mask_edge=self.mask_edge
                for i in self.hash_edge[json.loads(triggered[0]['prop_id'].split('.')[0])["label"]]["data"]:
                    new_mask_edge[i]=0
                self.hash_edge[json.loads(triggered[0]['prop_id'].split('.')[0])["label"]]["selected"]=0
                self.mask_edge=copy.deepcopy(new_mask_edge)
                return {'height':'5vh','margin':"2%",'display':'flex','align-items': 'center',"opacity":"0.2"}
    
    
        #TODO : If we click rapidly on multiple links callbacks will be fired before the 
        # one before had finished
    
        @app.callback(
            Output({"index": MATCH,"type": "node_legend","label":MATCH}, "style"),
            Input({"index": MATCH,"type": "node_legend","label":MATCH}, "n_clicks"),
            State('stored-data-edges','data'),
        )
        def node_selction(n,data_edge):
            triggered = dash.callback_context.triggered

            if n is None :
                return {'height':'5vh','margin':"2%",'display':'flex','align-items': 'center'}
            elif n % 2 ==0:
                n_mask_node=self.mask_node
                n_mask_edge=self.mask_edge
                D=pd.DataFrame(data_edge)
                for i in self.hash_node[json.loads(triggered[0]['prop_id'].split('.')[0])["label"]]["data"]:
                    n_mask_node[i]=1
                

                for i in self.hash_node[json.loads(triggered[0]['prop_id'].split('.')[0])["label"]]["data"]:

                    for ind in D.index[D["destination"]==i]:
                        if 'type' in D:
                            if self.hash_edge[D['type'].iloc[ind]]["selected"]==1 and n_mask_node[D["source"][ind]]==1:
    
                                n_mask_edge[ind]=1
                        else:
                            if n_mask_node[D["source"][ind]]==1:
                                n_mask_edge[ind]=1


                    for ind in D.index[D["source"]==i]:
                        if 'type' in D:
                            if self.hash_edge[D['type'].iloc[ind]]["selected"]==1 and n_mask_node[D["destination"][ind]]==1:
                                n_mask_edge[ind]=1
                        else:
                            if n_mask_node[D["destination"][ind]]==1:
                                n_mask_edge[ind]=1
                self.hash_node[json.loads(triggered[0]['prop_id'].split('.')[0])["label"]]["selected"]=1

                self.mask_node=copy.deepcopy(n_mask_node)
                self.mask_edge=copy.deepcopy(n_mask_edge)
                return {'height':'5vh','margin':"2%",'display':'flex','align-items': 'center'}
            
            else:
                n_mask_node=self.mask_node
                n_mask_edge=self.mask_edge
                D=pd.DataFrame(data_edge)
                for i in self.hash_node[json.loads(triggered[0]['prop_id'].split('.')[0])["label"]]["data"]:
                    n_mask_node[i]=0
                    for ind in D.index[D["destination"]==i]:
                        n_mask_edge[ind]=0

                    for ind in D.index[D["source"]==i]:
                        n_mask_edge[ind]=0

                self.hash_node[json.loads(triggered[0]['prop_id'].split('.')[0])["label"]]["selected"]=0
                self.mask_node=copy.deepcopy(n_mask_node)
                self.mask_edge=copy.deepcopy(n_mask_edge)
                return {'height':'5vh','margin':"2%",'display':'flex','align-items': 'center',"opacity":"0.2"}
    
