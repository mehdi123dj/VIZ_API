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
from ML_scripts.MachineLearning import MachineLearning
import dash_bootstrap_components as dbc
import dash_daq as daq
import base64
import datetime
import io
import dash_cytoscape as cyto
import math
import numpy as np
from dash import dash_table


class CreateElements():
    r"""
    A class that is managing all the interaction between components and windows and return 
    all the components and callbacks to the main frame
    
    Args:
        There is no args all the incoming data are controlled by the dcc.Upload component 
        which id is 'upload-data'
        
    """

    def __init__(self):
        
        self.cyto=CytoView()
        
        self.CP=ControlPanel() 
        self.color=ColorMap()
        # Container for the url gestion
        self.location=dcc.Location(id="url")
        
        # Container for nav bar 
        self.dashboard = dbc.NavbarSimple(
            children=[
                html.Img(src = "assets/favicon.ico", height= "60px",style={'transform': 'translateX(-50%)', 'left': '50%', 'position': 'absolute'}),
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Visualization", href="/visualization", active="exact")
                ],
            brand="Knowareness",
            color="dark",
            dark=True,
            )
        
        # Container for all that would be displayed in the first page
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
                html.Div(
                    children=[
                        dcc.Store(id='stored-data-edges', data={}),
                        dcc.Store(id='stored-data-nodes',data={}),
                        html.Div(id='output-datatable',
                                 children=[]
                            ),
                        html.Div(
                            children=[    
                                html.Div(
                                    children=[
                                        html.H6("Calculate position :",style={'display':'inline-block','vertical-align':'middle'}),
                                        daq.BooleanSwitch(id='bt-position',on=False,style={'display':'inline-block','position':'relative','margin-left':'2px','margin-right':'20px'}),
                                        ],
                                    id='position',
                                    style={'display':'none'}),
                                
                                html.Div(
                                    children=[
                                        html.H6("Directed graph :",style={'display':'inline-block','vertical-align':'middle'}),
                                        daq.BooleanSwitch(id='bt-oriented',on=False,style={'display':'inline-block','position':'relative','margin-left':'2px','margin-right':'20px'}),
                                        ],
                                    id='oriented',
                                    style={'display':'none'}),
                                
                                html.Div(
                                    children=[
                                        html.H6("Learn Graph node classification :",style={'display':'inline-block','vertical-align':'middle','margin-left':'20px'}),
                                        daq.BooleanSwitch(id='bt-learning',on=False,style={'display':'inline-block','position':'relative','margin-left':'2px'})
                                        ],
                                    id='learning',
                                    style={'display':'none'})
                                ],style={'textAlign': 'center','margin':'1em'}),
                        
                        html.Div(
                            children = [
                                html.Button('Launch Learning',id='bt-learning-launch',style={'position':'relative'})
                                        ],
                            style={'textAlign': 'center','margin':'1em'}),
                        ],
                    )
            ],
            id="div-home",style={'display':'none'})
        
        self.graph=html.Div(
                    html.Div(
                        children=[
                                html.Div(
                                    cyto.Cytoscape(
                                    id='cytoscape',
                                    layout={'name': 'preset'},
                                    elements=[],
                                    stylesheet=[],
                                    style={'width': '100%', 'height': '86.5vh','position': 'absolute','top':'0px',
                                            'left':'0px','z-index': '999'},
                                    minZoom=0.01,
                                    maxZoom=10,
                                    wheelSensitivity=0.1,
                                    boxSelectionEnabled=True
                                    ),# responsive=True
                                    style={
                                            'z-index':'100',
                                            'top':'0px',
                                            'left':'0px'}),
            
                                html.Button('Reset View', id='bt-reset-view',style={'position':'absolute','z-index':'10000','right':'1em','top':'1em'}),
                                html.Button('Reset Stylesheet', id='bt-reset-stylesheet',style={'position':'absolute','z-index':'10000','right':'1em','top':'3em'}),
                            
                            ],
                        id='cytoscape-elements',
                        style={'position': 'relative','z-index': '100'},
                        ),
                style={
                    'position': 'fixed',
                    'width': '75%',
                    'display':'inline-block',
                    'verticalAlign': 'top',
                })
        
        # Container for the graph visualization page
        self.visualization=html.Div(id='div-visualization',children=[],style={'display':'none'})

        
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
            
            def out(data):
                df=pd.DataFrame(data)
                return html.Div([
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
                ],style={'width': '48%','display':'inline-block','margin':'1%'})
            
            if u==True:
                for elem in L[0]:
                    div=out(elem[0])
                    if 'id' in elem[0][0]: #check if it is the dataframe concerning the nodes
                        computable="feature" in elem[0][0] and "class" in elem[0][0]
                        data_nodes=elem[0]
                    else:
                        data_edges=elem[0]
                    M.append(div)           

            else:
                div=out(L[0])
                if 'id' in L[0][0]: #check if it is the dataframe concerning the nodes
                    computable="feature" in L[0][0] and "class" in L[0][0]
                    data_nodes=L[0]
                else:
                    data_edges=L[0]
                M.append(div)
        return computable,M,data_nodes,data_edges

    def generate_display_tab(self,tab):
        
        def display_tab(pathname):
            # print(pathname is None or pathname == '/')
            if tab == 'div-home' and (pathname is None or pathname == '/'):
                print("home, tab :"+str(tab))
                print(pathname)
                return {}
            elif tab == 'div-visualization' and pathname == '/visualization':#{}'.format(tab):
                print("visu, tab :"+str(tab))
                print(pathname)
                return {}
            else:
                print("else")
                return {'display': 'none'}
        return display_tab

    def get_callbacks(self,app):

        cyto=self.cyto
        CP=self.CP
        color=self.color
        
        
        for tab in ['div-home', 'div-visualization']:
            app.callback(Output(tab, 'style'), [Input('url', 'pathname')])(
                self.generate_display_tab(tab)
            )


        @app.callback(Output('output-datatable', 'children'),
                      Output('position', 'style'),
                      Output('learning', 'style'),
                      Output('oriented', 'style'),
                      Output('stored-data-nodes', 'data'),
                      Output('stored-data-edges', 'data'),
                      Input('upload-data', 'contents'),
                      State('upload-data', 'filename'),
                      State('upload-data', 'last_modified'))
        def update_output(list_of_contents, list_of_names, list_of_dates):
            if list_of_contents is not None:
                computable,children,data_nodes,data_edges = self.parse_contents(list_of_contents, list_of_names, list_of_dates)#(c, n, d) for c, n, d in  zip(list_of_contents, list_of_names, list_of_dates)
                if computable:
                    print("here")
                    return [children,{'display':'inline-block'},{'display':'inline-block'},{'display':'inline-block'},data_nodes,data_edges]
                else :
                    return [children,{'display':'none'},{'display':'none'},{'display':'inline-block'},data_nodes,data_edges]
            else:
                return [dash.no_update,{'display':'none'},{'display':'none'},{'display':'none'},dash.no_update,dash.no_update]
                      
        
        @app.callback(
            Output('bt-learning-launch', 'style'),
            Input('bt-learning', 'on'),
        )
        def is_visible_launchLearningButton(on):
            
            x = "{}".format(on)
            if  x == "True":
                return {'position':'relative'}
            else:
                return {'display':'none','position':'relative'}
            
            
        @app.callback(Output('div-visualization', 'children'),
                      Input('output-datatable', 'children'),
                      Input('bt-learning-launch', 'n_clicks'),
                      Input('bt-learning','on'),
                      Input('bt-position','on'),
                      State('stored-data-nodes','data'),
                      State('stored-data-edges','data'),
                      )
        def make_graphs(child,click,bt_learn,bt_pos,data_nodes,data_edges):

            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            triggered = dash.callback_context.triggered[0]['value']

            if 'output-datatable' in changed_id:
                if 'positionX' and 'positionY' in data_nodes[0]:
                    color(data_edges,data_nodes)
                    CP(color.edge_legend,color.node_legend,data_edges,data_nodes)
                    cyto(data_nodes,data_edges,CP,color.stylesheet)

                    return html.Div(children=[
                        CP.create_CP(),
                        self.graph
                        ])
                else:
                    return dash.no_update

            elif 'bt-learning-launch' in changed_id:
                if triggered==None:
                    return dash.no_update
                else :
                    ML=MachineLearning(data_nodes,data_edges,bt_pos)
                    data_nodes = ML()
                    if 'positionX' and 'positionY' in data_nodes[0]:
                        color(data_edges,data_nodes,classif=True)
                        CP(color.edge_legend,color.node_legend,data_edges,data_nodes)
                        cyto(data_nodes,data_edges,CP,color.stylesheet)

                        div=html.Div(children=[
                            CP.create_CP(),
                            self.graph
                            ])
                        return div
                    else:
                        return html.Div([
                            html.H6("No positional values put calculate button position to true")
                            ])

            else :
                x = "{}".format(bt_learn)
                if x == "False":
                    if data_nodes=={}:
                        return html.Div([
                            html.H6("Not any data uploaded")
                            ])
                    elif 'positionX' and 'positionY' in data_nodes[0]:
                        color(data_edges,data_nodes)
                        CP(color.edge_legend,color.node_legend,data_edges,data_nodes)
                        cyto(data_nodes,data_edges,CP,color.stylesheet)
                        return html.Div(children=[
                            CP.create_CP(),
                            self.graph
                            ])
                    else :
                        return html.Div([
                            html.H6("No positional values try to use the features if you have some")
                            ])
                else :
                    return dash.no_update

        cyto.get_callbacks(app)
        CP.get_callbacks(app)

