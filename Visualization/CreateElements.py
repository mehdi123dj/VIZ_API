# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 13:11:39 2022

@author: remit
"""

import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import pandas as pd
from FileConvert import csv_to_df, gml_to_df
from ControlPanel import ControlPanel
from CytoView import CytoView
from ColorMap import ColorMap
from MachineLearning import MachineLearning
import dash_bootstrap_components as dbc
import dash_daq as daq
import base64
import datetime
import io
import math
import numpy as np
from dash import dash_table


class CreateElements():
    
    
    def __init__(self):
    
        self.dashboard = dbc.NavbarSimple(
            children=[
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Visualization", href="/visualization", active="exact")
                ],
            brand="Graph visualization app",
            color="dark",
            dark=True,
            )

        self.location=dcc.Location(id="url")
        
        self.home=html.Div([dcc.Upload(
                    className='Links',
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files'),
                        ' of links between nodes'
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',

                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
            
                html.Div(id='output-datatable'),
                html.Div(id='choice-for-learning')

            ],
            id="home",style={'display':'none'})
        
        self.visualization=html.Div(id='visualization',style={'display':'none'})

        
    def __call__(self):

        return [self.location,self.dashboard,self.home,self.visualization]

    def parse_contents(self,list_of_contents, list_of_names, list_of_dates):
        M=[]
        for (contents,filename,date) in zip(list_of_contents,list_of_names,list_of_dates):
            content_type, content_string = contents.split(',')
    
            
            decoded = base64.b64decode(content_string)
            
            L=[]
            u=False
            try:
                
                if 'csv' in filename:
                    # Assume that the user uploaded a CSV file
                    L.append(csv_to_df(decoded.decode('utf-8')))
                elif 'xls' in filename:
                    # Assume that the user uploaded an excel file
                    L.append(csv_to_df(io.BytesIO(decoded)))
    
                elif 'gml' in filename:
                    # Assume that the user uploaded a graph modelling language based file
                    L.append(gml_to_df(decoded.decode('utf-8')))
                    u=True
    
                    
            except Exception as e:
                print(e)
                return html.Div([
                    'There was an error processing this file.'
                ])
            
    

            def out(store):
                df=pd.DataFrame.from_dict(store.data)
                if 'positionX' in df:
                    print(type(df["feature"][0]))
                    print(type(df["feature"][0][0]))

                return df,html.Div([
                    html.H5(filename),
                    html.H6(datetime.datetime.fromtimestamp(date)),
    
                    dash_table.DataTable(
                        data=df.applymap(str).to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in df.columns],
                        style_cell={'textAlign': 'center'},
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        },
                        style_table={'overflowX': 'auto'},
                        page_size=10
                    ),
                    store
                ],style={'width': '48%','display':'inline-block','margin':'1%'})
            
            
    
            if u==True:
                for elem in L[0]:
                    df_temp,div=out(elem[0])
                    if 'positionX' in df_temp: #check if it is the dataframe concerning the nodes
                        df=df_temp
                    M.append(div)           

            
            else:
                df_temp,div=out(L[0])
                if 'positionX' in df_temp: #check if it is the dataframe concerning the nodes
                    df=df_temp
                M.append(div)
        return df,M


    def generate_display_tab(self,tab):
        def display_tab(pathname):
            if tab == 'home' and (pathname is None or pathname == '/'):
                return {'display': 'block'}
            elif pathname == '/{}'.format(tab):
                return {'display': 'block'}
            else:
                return {'display': 'none'}
        return display_tab



    def get_callbacks(self,app):

        cyto=CytoView()
        CP=ControlPanel() 

        for tab in ['home', 'visualization']:
            app.callback(Output(tab, 'style'), [Input('url', 'pathname')])(
                self.generate_display_tab(tab)
            )


        @app.callback(Output('output-datatable', 'children'),
                      Input('upload-data', 'contents'),
                      State('upload-data', 'filename'),
                      State('upload-data', 'last_modified'))
        def update_output(list_of_contents, list_of_names, list_of_dates):
            if list_of_contents is not None:
                df,children = self.parse_contents(list_of_contents, list_of_names, list_of_dates)#(c, n, d) for c, n, d in  zip(list_of_contents, list_of_names, list_of_dates)
                L = list(df['class'].unique())
                print(L)
                print([type(elem) for elem in L])
                L = [elem for elem in L if elem!='nan']
                children.append(html.Div(
                                    children=[                
                                        html.H6("Directed graph :",style={'display':'inline-block','vertical-align':'middle'}),
                                        daq.BooleanSwitch(id='bt-oriented', on=False,style={'display':'inline-block','position':'relative','margin-left':'2px','margin-right':'20px'}),
                                                            
                                        html.H6("Learn Graph node classification :",style={'display':'inline-block','vertical-align':'middle','margin-left':'20px'}),
                                        daq.BooleanSwitch(id='bt-learning', on=False,style={'display':'inline-block','position':'relative','margin-left':'2px'})
                                        ],style={'textAlign': 'center','margin':'1em'}))
                children.append(html.Div(
                    children = [
                                # dcc.RadioItems(L, 
                                #                L[0],
                                #                id='choose-node-class',
                                #                inline=True,
                                #                style={'display':'inline-block','vertical-align':'middle','margin-right':'10px'}),
                                html.Button('Launch Learning',id='bt-learning-launch',style={'display':'inline-block','position':'relative'})
                                ],
                    style={'textAlign': 'center','margin':'1em','display':'none'},
                    id='choice-learning-div'))
                return children
                      
        
        @app.callback(
            Output('choice-learning-div', 'style'),
            Input('bt-learning', 'on'),
        )
        def is_visible_radioItems(on):
            print(on)
            x = "{}".format(on)
            if  x == "True":
                return {'textAlign': 'center','margin':'1em',}
            else:
                return {'textAlign': 'center','margin':'1em','display':'none'}
            
            
        @app.callback(Output('visualization', 'children'),
                      Input('bt-learning-launch', 'n_clicks'),
                      Input('bt-learning','on'),
                      State('stored-data-nodes','data'),
                      State('stored-data-edges','data'),
                      State('choose-node-class','value'),
                      )
        def make_graphs(click,on,data_nodes,data_edges,node_class):

            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            print(changed_id)
            color=ColorMap()
            triggered = dash.callback_context.triggered[0]['prop_id'].split('.')
            print(triggered)
            if 'bt-learning-launch' in changed_id:

                if triggered==None:
                    return dash.no_update
                else :
                    # print(data_nodes)
                    ML=MachineLearning(data_nodes,data_edges)
                    ML()
                    color(data_edges,data_nodes,node_class)
                    CP(color.edge_legend,color.node_legend,data_edges,data_nodes)
                    cyto(data_nodes,data_edges,CP)
                    div=html.Div([
                        CP.create_CP(),
                        cyto.create_cyto(color.stylesheet)
                        ])
                    
                    return div
        
            else :
                x = "{}".format(on)

                if x == "False":
                    color(data_edges,data_nodes)
                    CP(color.edge_legend,color.node_legend,data_edges,data_nodes)
                    cyto(data_nodes,data_edges,CP)
                    return html.Div([
                        CP.create_CP(),
                        cyto.create_cyto(color.stylesheet)
                        ])
                else :
                    return dash.no_update

            
        cyto.get_callbacks(app)
        CP.get_callbacks(app)






        
        
        



