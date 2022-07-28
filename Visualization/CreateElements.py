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
from dash import dash_table
cyto.load_extra_layouts()


class CreateElements():
    r"""
    A class that is managing all the interaction between components and windows and return 
    all the components and callbacks to the main frame

    Args:
        There is no args all the incoming data are controlled by the dcc.Upload component 
        which id is 'upload-data'

    """

    def __init__(self):

        # Initialization of the app class that would be used afterward to interact
        self.cyto = CytoView()
        self.CP = ControlPanel()
        self.color = ColorMap()

        # Container for the url gestion
        self.location = dcc.Location(id="url")

        # Container for nav bar
        self.dashboard = dbc.NavbarSimple(
            children=[
                html.Img(src="assets/favicon.ico", height="60px", style={
                         'transform': 'translateX(-50%)', 'left': '50%', 'position': 'absolute'}),
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Visualization",
                            href="/visualization", active="exact")
            ],
            brand="Knowareness",
            color="dark",
            dark=True,
        )

        # Container for all that would be displayed in the first page
        self.home = html.Div([dcc.Upload(
            id='upload-data',
            disable_click=True,
            children=html.Div([
                'Drag and Drop file(s) of edges and nodes ',
                
                dbc.Badge(u'\U0001f6c8', color="light",id="info-badge",style={'z-index': '10000'}),
                dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("INPUT FILES FORMAT")),
                                dbc.ModalBody(dcc.Markdown('''
                                                They are as follow :
                                                
                                                * **CSV and XLS files**, you will have to upload edges and nodes file simultaneously in the drop zone, otherwise will not work.
                                                
                                                    * File for edges should have the same format of header as shown below (you could omit non compulsory columns) and registered as csv/xls. You are force to furnish values for the **source** and **target** you can also provide values for **class** and **data** but it is not mandatory and sparse information could be given. A solution could be to add nothing, just let it empty (as shown below).
                                                    ```
                                                    source,target,class,data
                                                    34,4,professional,Knowing since : 3 years
                                                    1,21,friend,Knowing since : 97 years
                                                    20,12,friend,Knowing since : 9 years
                                                    3,0,friend,Knowing since : 51 years
                                                    6,38,family,Knowing since : 3 years
                                                    45,4,professional,Knowing since : 7 years
                                                    0,8,family,Knowing since : 3 years
                                                    ```
                                                
                                                    * File for nodes should have the same format of header as shown below (you could omit non compulsory columns) and registered as csv/xls.You are force to furnish values for the **id** you can also provide values for **positionX**,**positionY**,**feature**, **class** but you will have to furnish value for all rows!  **data** column is not mandatory and you can provide sparse information. <A solution could be to add nothing, just let it empty (as shown below).>
                                                    ```
                                                    id,positionX,positionY,class,data,feature
                                                    0,59.17180618694536,22.11030522902449,teenager,"Name : ludivine, age : 65","[69.33928670214559, 75.45925097633007, 70.99528587804748]"
                                                    1,-96.05151980887148,-70.4455325019663,teenager,"Name : fabrice, age : 78","[96.69387532958712, 69.9360406529872, 74.12491979334999]"
                                                    2,33.53531243249327,5.4884938927682185,adult,"Name : fabrice, age : 34","[11.618561313551945, 14.80660556644035, 30.668334158786944]"
                                                    3,-28.93342830907102,5.372990605701716,adult,"Name : matthieu, age : 34","[25.44111693575362, 2.1404425396293245, 19.5873407260785]"
                                                    4,-14.80054648587111,-55.81053799438567,teenager,"Name : matthieu, age : 55","[82.0134713406511, 75.87393548272328, 91.15490976049222]"
                                                    5,87.89876740468642,29.610566777499315,adult,"Name : henri, age : 65","[21.614522662913647, 15.749883206784437, 30.730064306816665]"
                                                    6,-54.64595487735493,-17.741161229561484,child,"Name : pascale, age : 20","[46.63956809476848, 48.89752997060593, 49.8082400003897]"
                                                    ```
                                                
                                                * **GML Files**
                                                  File should have the same form as shown below and registered as gml. You are force to furnish values for the **source** and **target** for the edges and **id** for the nodes. You can provide **positionX**,**positionY**,**features** but you will have to furnish for all rows! For **class** and **data** sparse information could be given, you will have to add **'NaN'** when no information is given (as shown below).
                                                   
                                                    ```
                                                      graph [
                                                        multigraph 1
                                                          node [
                                                            id 0
                                                            label "0"
                                                            positionX 59.17180618694536
                                                            positionY 22.11030522902449
                                                            class "teenager"
                                                            data "Name : ludivine, age : 65"
                                                            feature "[69.33928670214559, 75.45925097633007, 70.99528587804748]"
                                                          ]
                                                          node [
                                                            id 1
                                                            label "1"
                                                            positionX -96.05151980887148
                                                            positionY -70.4455325019663
                                                            class "nan"
                                                            data "Name : fabrice, age : 78"
                                                            feature "[96.69387532958712, 69.9360406529872, 74.12491979334999]"
                                                          ]
                                                          node [
                                                            id 2
                                                            label "2"
                                                            positionX 33.53531243249327
                                                            positionY 5.4884938927682185
                                                            class "adult"
                                                            data "Name : fabrice, age : 34"
                                                            feature "[11.618561313551945, 14.80660556644035, 30.668334158786944]"
                                                          ]
                                                          node [
                                                            id 3
                                                            label "3"
                                                            positionX -28.93342830907102
                                                            positionY 5.372990605701716
                                                            class "adult"
                                                            data "nan"
                                                            feature "[25.44111693575362, 2.1404425396293245, 19.5873407260785]"
                                                          ]
                                                          ...
                                                    
                                                          edge [
                                                            source 0
                                                            target 2
                                                            key 0
                                                            class "professional"
                                                            data "Knowing since : 23 years"
                                                          ]
                                                          edge [
                                                            source 0
                                                            target 2
                                                            key 1
                                                            class "professional"
                                                            data "Knowing since : 23 years"
                                                          ]
                                                          edge [
                                                            source 0
                                                            target 11
                                                            key 0
                                                            class "nan"
                                                            data "Knowing since : 9 years"
                                                          ]
                                                          edge [
                                                            source 0
                                                            target 11
                                                            key 1
                                                            class "friend"
                                                            data "Knowing since : 9 years"
                                                          ]
                                                          ...
                                                        ]
                                                        
                                                            ''')),
                            ],
                            id="modal",
                            scrollable=True,
                            centered=True,
                            is_open=False,
                            size='xl'
                        ),
            ]),
            style={
                'width': '100%',
                'height': '5vmin',
                'lineHeight': '5vmin',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
            html.Div(
            children=[
                dcc.Store(id='stored-data-edges', data={}),
                dcc.Store(id='stored-data-nodes', data={}),
                html.Div(id='output-datatable',
                         children=[]
                         ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H6("Calculate position :", style={
                                    'display': 'inline-block', 'vertical-align': 'middle'}),
                                daq.BooleanSwitch(id='bt-position', on=False, style={
                                                  'display': 'inline-block', 'position': 'relative', 'margin-left': '2px', 'margin-right': '20px'}),
                            ],
                            id='position',
                            style={'display': 'none'}),

                        html.Div(
                            children=[
                                html.H6("Directed graph :", style={
                                    'display': 'inline-block', 'vertical-align': 'middle'}),
                                daq.BooleanSwitch(id='bt-oriented', on=False, style={
                                                  'display': 'inline-block', 'position': 'relative', 'margin-left': '2px', 'margin-right': '20px'}),
                            ],
                            id='oriented',
                            style={'display': 'none'}),

                        html.Div(
                            children=[
                                html.H6("Learn Graph node classification supervised :", style={
                                        'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '20px'}),
                                daq.BooleanSwitch(id='bt-learning-node-deep', on=False, style={
                                                  'display': 'inline-block', 'position': 'relative', 'margin-left': '2px'})
                            ],
                            id='learning-node-deep',
                            style={'display': 'none'}),
                        
                        html.Div(
                            children=[
                                html.H6("Learn Graph node classification unsupervised:", style={
                                        'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '20px'}),
                                daq.BooleanSwitch(id='bt-learning-node-unsupervised', on=False, style={
                                                  'display': 'inline-block', 'position': 'relative', 'margin-left': '2px'})
                            ],
                            id='learning-node-unsupervised',
                            style={'display': 'none'}),


                        html.Div(
                            children=[
                                html.H6("Learn Graph edge prediction :", style={
                                        'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '20px'}),
                                daq.BooleanSwitch(id='bt-learning-edge', on=False, style={
                                                  'display': 'inline-block', 'position': 'relative', 'margin-left': '2px'})
                            ],
                            id='learning-edge',
                            style={'display': 'none'})
                    ], style={'textAlign': 'center', 'margin': '1em'}),

                html.Div(
                    children=[

                        html.Button(
                            'Launch Learning', id='bt-learning-launch', style={'display': 'none','position': 'relative'})
                    ],
                    style={'textAlign': 'center', 'margin': '1em'}),
            ],
        )
        ],
            id="div-home", style={'display': 'none'})

        # Container for the cytoscape graph view
        self.graph = html.Div(
            html.Div(
                children=[
                    html.Div(
                        cyto.Cytoscape(
                            id='cytoscape',
                            layout={'name': 'preset'},
                            elements=[],
                            stylesheet=[],
                            style={'width': '100%', 'height': '86.5vh', 'position': 'absolute', 'top': '0px',
                                   'left': '0px', 'z-index': '999'},
                            minZoom=0.01,
                            maxZoom=10,
                            # To be activated need to modify the code inside dash cytosacpe but could block the code from running while in release mode
                            # wheelSensitivity=0.05,
                            boxSelectionEnabled=True
                        ),  # responsive=True
                        style={
                            'z-index': '100',
                            'top': '0px',
                            'left': '0px'}),

                    html.Button('Reset View', id='bt-reset-view', style={
                                'position': 'absolute', 'z-index': '10000', 'right': '1em', 'top': '1em'}),
                    html.Button('Reset Stylesheet', id='bt-reset-stylesheet', style={
                                'position': 'absolute', 'z-index': '10000', 'right': '1em', 'top': '3em'}),

                ],
                id='cytoscape-elements',
                style={'position': 'relative', 'z-index': '100'},
            ),
            style={
                'position': 'fixed',
                'width': '75%',
                'display': 'inline-block',
                'verticalAlign': 'top',
            })

        # Container for the graph visualization page
        self.visualization = html.Div(
            id='div-visualization', children=[], style={'display': 'none'})

    def __call__(self):
        r"""
            Function that return the 4 global components to the dash layout

            Returns:
                self.location(dcc.Location) : Container for the url gestion

                self.dashboard(dbc.NavbarSimple) : Container for the navigator bar in top of the app

                self.home(div) : Container for the home page

                self.visualization(div) : Container for the graph visualization page

        """

        return [self.location, self.dashboard, self.home, self.visualization]

    def parse_contents(self, list_of_contents, list_of_names, list_of_dates):
        r"""
            Function that parse the files that were uploaded, uses side functions that could be found in FileConvert.py

            Args:
                list_of_contents (string): 
                    Content of the uploaded files
                list_of_names (string):
                    Name of the uploaded files
                list_of_dates (string):
                    Information about the date at which the files were created

            Returns:
                M (list): List of div of dataTable elements with the name of the file and its date


        """

        M = []
        for (contents, filename, date) in zip(list_of_contents, list_of_names, list_of_dates):
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            L = []
            u = False
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
                    u = True

            except Exception as e:
                print(e)
                return html.Div([
                    'There was an error processing this file.'
                ])

            def out(data):
                df = pd.DataFrame(data)
                return html.Div([
                    html.H6(filename),
                    #html.P(datetime.datetime.fromtimestamp(date),style={'font-size': '1.2vmin'}),
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
                        page_size=8
                    ),
                ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'})

            if u == True:
                for elem in L[0]:
                    div = out(elem[0])
                    if 'id' in elem[0][0]:  # check if it is the dataframe concerning the nodes
                        computable = "feature" in elem[0][0] #and "class" in elem[0][0]
                        supervised = "class" in elem[0][0]
                        data_nodes = elem[0]
                    else:
                        data_edges = elem[0]
                    M.append(div)

            else:
                div = out(L[0])
                if 'id' in L[0][0]:  # check if it is the dataframe concerning the nodes
                    computable = "feature" in L[0][0] #and "class" in L[0][0]
                    supervised = "class" in L[0][0]
                    data_nodes = L[0]
                else:
                    data_edges = L[0]
                M.append(div)

        return computable,supervised, M, data_nodes, data_edges

    def generate_display_tab(self, tab):
        r"""
            Function that manage which page should be outputed

            Returns:
                tab (string): Name of the div id of the desired page to output

        """
        def display_tab(pathname):
            if tab == 'div-home' and (pathname is None or pathname == '/'):
                return {}
            elif tab == 'div-visualization' and pathname == '/visualization':
                return {}
            else:
                return {'display': 'none'}
        return display_tab

    def get_callbacks(self, app):

        cyto = self.cyto
        CP = self.CP
        color = self.color



        @app.callback(Output("modal", "is_open"),
                       Input('info-badge', 'n_clicks'),
                       State("modal", "is_open")
                       )
        def output_info(n,is_open):
            if n:
                return not is_open
            return is_open

        for tab in ['div-home', 'div-visualization']:
            app.callback(Output(tab, 'style'), [Input('url', 'pathname')])(
                self.generate_display_tab(tab)
            )

        @app.callback(Output('output-datatable', 'children'),
                      Output('position', 'style'),
                      Output('position', 'on'),
                      Output('learning-node-deep', 'style'),
                      Output('learning-node-unsupervised', 'style'),
                      Output('learning-edge', 'style'),
                      Output('oriented', 'style'),
                      Output('stored-data-nodes', 'data'),
                      Output('stored-data-edges', 'data'),
                      Input('upload-data', 'contents'),
                      State('upload-data', 'filename'),
                      State('upload-data', 'last_modified'))
        def update_output(list_of_contents, list_of_names, list_of_dates):
            r"""
                Function that parse the files that were uploaded and update a lot of component children,
                    in particular register the data that were imported in stored-data-nodes and stored-data-edges

                Args:
                    list_of_contents (string): 
                        Content of the uploaded files
                    list_of_names (string):
                        Name of the uploaded files
                    list_of_dates (string):
                        Information about the date at which the files were created

                Returns:
                    List updating the outputed components of the form :
                        [output-datatable children,  position style,
                          learning-node style, learning-edge style, oriented style,
                          stored-data-nodes data, stored-data-edges data]

            """
            if list_of_contents is not None:
                computable, supervised, children, data_nodes, data_edges = self.parse_contents(
                    list_of_contents, list_of_names, list_of_dates)
                if computable & supervised:
                    return [children, {'display': 'inline-block'},False, {'display': 'inline-block'},{'display': 'inline-block'}, {'display': 'inline-block'}, {'display': 'inline-block'}, data_nodes, data_edges]
                elif computable :
                    return [children, {'display': 'none'},True, {'display': 'none'},{'display': 'inline-block'}, {'display': 'none'}, {'display': 'inline-block'}, data_nodes, data_edges]
                else:
                    return [children, {'display': 'none'},False, {'display': 'none'}, {'display': 'none'},{'display': 'none'}, {'display': 'inline-block'}, data_nodes, data_edges]
            else:
                return [dash.no_update, {'display': 'none'},False, {'display': 'none'}, {'display': 'none'},{'display': 'none'}, {'display': 'none'}, dash.no_update, dash.no_update]

        @app.callback(
            Output('bt-learning-launch', 'style'),
            Output('bt-learning-node-deep', 'on'),
            Output('bt-learning-node-unsupervised', 'on'),
            Output('bt-learning-edge', 'on'),
            
            Input('upload-data', 'contents'),
            Input('bt-learning-node-deep', 'on'),
            Input('bt-learning-node-unsupervised', 'on'),
            Input('bt-learning-edge', 'on'),
            State('stored-data-edges', 'data'),
        )
        def is_visible_launchLearningButton(contents, on_node_deep, on_node_unsupervised, on_edge, data_edges):
            r"""
                Function that make visible/unvisible the launch learning button

                Args:
                    contents (string): when data is reuploaded trigger the function to reset all the buttons on False
                    
                    on_node_deep (string): String of boolean object

                    on_node_unsupervised (string): String of boolean object

                    on_edge (string): String of boolean object

                    data_edge (dictionnary): See other functions in which define

                Returns:
                    Update the style component of the button for it to be visible or not

            """
            changed_id = [p['prop_id']
                          for p in dash.callback_context.triggered][0]              
            node_deep = "{}".format(on_node_deep)
            node_unsupervised = "{}".format(on_node_unsupervised)
            edge = "{}".format(on_edge)
            if 'upload-data' in changed_id:
                return [       
                        {'display': 'none', 'position': 'relative'},
                        False,
                        False,
                        False,
                        ]    
            elif ('bt-learning-edge' in changed_id) and edge == "True":

                return [
                        {'margin-left': '20px', 'position': 'relative', 'display': 'inline-block', 'vertical-align': 'middle'},
                        False,
                        False,
                        dash.no_update]

            elif ('bt-learning-node-deep' in changed_id) and node_deep == "True":
                return [
                        {'position': 'relative'},
                        dash.no_update,
                        False,
                        False,
                        ]               
            elif ('bt-learning-node-unsupervised' in changed_id) and node_unsupervised == "True":
                return [
                        {'position': 'relative'},
                        False,
                        dash.no_update,
                        False,
                        ]      
            
            else:
                return [
                        {'display': 'none', 'position': 'relative'},
                        False,
                        False,
                        False,
                        ]    

        @app.callback(Output('div-visualization', 'children'),
                      Input('output-datatable', 'children'),
                      Input('bt-learning-launch', 'n_clicks'),
                      Input('bt-learning-node-deep', 'on'),
                      Input('bt-learning-node-unsupervised', 'on'),
                      Input('bt-learning-edge', 'on'),
                      Input('bt-position', 'on'),
                      State('stored-data-nodes', 'data'),
                      State('stored-data-edges', 'data'),
                      )
        def make_graphs(child, click, bt_learn_node_deep, bt_learn_node_unsupervised,bt_learn_edge, bt_pos, data_nodes, data_edges):
            r"""
                Function that gather all the information needed to construct the graph and the control panel 
                it updates the corresponding class instances by using the functions designed in each of them

                Args:
                    child (div): Triggered when a change occur in the output-datatable component of the home page
                    id. when some data are uploaded

                    click (int): Button to launch a training of the model

                    bt_learn_node (string): String of a boolean value designed to allow the user to make the launch button appearing
                        and allow training on node classification

                    bt_learn_edge (string): String of a boolean value designed to allow the user to make the launch button appearing
                        and allow training on edge classification

                    bt_pos (string): String of a boolean value designed to allow the user to recalculate nodes positions depending
                        result of the model learned

                    data_nodes (list): A list of the following format, for each node:
                        {'id': int, 'positionX': float, 'positionY': float, 'class': str, 'data': str, 'feature': list of float}

                        id: The local id of a node | Compulsory

                        positionX, positionY : The position gave as input or compiled thanks to features | this is optional but nothing 
                            will appear if not provide.

                        class: A string which gives the class of the given node | Optionnal

                        feature: A list of float which give the embedding for a given node | Optionnal, not used for representation

                        data: String which gives some info about the node | Optionnal, used when clicking on a node to display info about it

                    data_edges (list): A list of the following format, for each edge:
                        {'source': int, 'target': int, 'data': str, 'class': str}

                        source: The id of the source node | Compulsory

                        target: The id of the taget node | Compulsory

                        data: String which gives some info about the edge | Optionnal, used when clicking on an edge to display info about it

                        class: A string which gives the class of the given edge | Optionnal

                Returns:
                    A div container in which all the visualization page is constructed

            """
            changed_id = [p['prop_id']
                          for p in dash.callback_context.triggered][0]
            triggered = dash.callback_context.triggered[0]['value']

            if 'output-datatable' in changed_id:
                if 'positionX' and 'positionY' in data_nodes[0]:
                    color(data_edges, data_nodes)
                    CP(color.edge_legend, color.node_legend, data_edges, data_nodes)
                    cyto(data_nodes, data_edges, CP, color.stylesheet)

                    return html.Div(children=[
                        CP.create_CP(),
                        self.graph
                    ])
                else:
                    return dash.no_update

            elif 'bt-learning-launch' in changed_id:
                if triggered == None:
                    return dash.no_update
                else:
                    if ('positionX' and 'positionY' in data_nodes[0]) or bt_pos:

                        ML = MachineLearning(
                            data_nodes, data_edges, bt_pos, bt_learn_node_deep, bt_learn_edge, bt_learn_node_unsupervised)
                        data_nodes,data_edges = ML()
                        color(data_edges, data_nodes, classif=True)
                        CP(color.edge_legend, color.node_legend,
                           data_edges, data_nodes)
                        cyto(data_nodes, data_edges, CP, color.stylesheet)

                        div = html.Div(children=[
                            CP.create_CP(),
                            self.graph
                        ])
                        return div
                    else:
                        return html.Div([
                            html.H6(
                                "No positional values put calculate button position to true")
                        ])

            else:
                if data_nodes == {}:
                    return html.Div([
                        html.H6("Not any data uploaded")
                    ])
                elif 'positionX' and 'positionY' in data_nodes[0]:
                    color(data_edges, data_nodes)
                    CP(color.edge_legend, color.node_legend,
                       data_edges, data_nodes)
                    cyto(data_nodes, data_edges, CP, color.stylesheet)
                    return html.Div(children=[
                        CP.create_CP(),
                        self.graph
                    ])
                else:
                    return html.Div([
                        html.H6(
                            "No positional values try to use the features if you have some")
                        ])
                
        cyto.get_callbacks(app)
        CP.get_callbacks(app)
