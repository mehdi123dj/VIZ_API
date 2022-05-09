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
from ControlPanel import ControlPanel
from CytoView import CytoView
from ColorMap import ColorMap
import dash_bootstrap_components as dbc
import dash_daq as daq
import base64
import datetime
import io
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
                        #'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
                html.Div(
                    children=[
                        html.H6("Directed graph :",style={'display':'inline-block','vertical-align':'middle'}),
                        daq.BooleanSwitch(id='bt-oriented', on=False,style={'display':'inline-block','position':'relative'})
                        
                        ],style={'textAlign': 'center','margin':'1em'})
                ,
            
                html.Div(id='output-datatable')
            ],
            id="home",style={'display':'none'})
        
        self.visualization=html.Div(id='visualization',style={'display':'none'})

        
    def __call__(self):

        return [self.location,self.dashboard,self.home,self.visualization]

    def parse_contents(self,contents, filename, date):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
                
            
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

        if 'Links' in filename or 'Edges' in filename:
            if "type" in df:
                df["type"]=df["type"].map(str)
            store=dcc.Store(id='stored-data-edges', data=df.to_dict('records'))

        if 'Nodes' in filename :
            if "type" in df:  
                df["type"]=df["type"].map(str)
            store=dcc.Store(id='stored-data-nodes', data=df.to_dict('records'))


        return html.Div([
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),

            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
                page_size=10
            ),
            store
        ],style={'width': '48%','display':'inline-block','margin':'1%'})


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
                children = [
                    self.parse_contents(c, n, d) for c, n, d in  zip(list_of_contents, list_of_names, list_of_dates)
                    ]
                return children
            
        @app.callback(Output('visualization', 'children'),
                      Input('output-datatable', 'children'),
                      State('stored-data-nodes','data'),
                      State('stored-data-edges','data'),
                      )
        def make_graphs(table,data_nodes,data_edges):
            if table !=None:
                color=ColorMap()
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






        
        
        



