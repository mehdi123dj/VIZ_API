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
from dash.dependencies import Input, Output, MATCH
import dash_cytoscape as cyto
cyto.load_extra_layouts()


class ControlPanel():
    r"""
    A class that is designed to create the control panel that is displayed in the visualization page,
    manage the clickable interaction for nodes/edges displayed and also to output the informations of 
    the nodes and edges we could click one. Furthemore the class will also have as variables the mask
    for nodes and edges that have to be displayed regarding the actual selected nodes and edges buttons
        
    """

    def __init__(self):
        self.styles = {
            'tab': {
                'height': '78.5vh',
                'maxHeight': '78.5vh',
                'overflow-y': 'scroll',
                'background-color': '#c7c7c7',
                'padding': '2%'
            }
        }

    def __call__(self, edge_legend, node_legend, data_edges, data_nodes):
        r"""
            Creation of the intial value for edge_mask and node_mask
            
            Args:
                edge_legend (list): List of tuples relative to edges [string of the hex color,string of the name of the class]
                    
                node_legend (list): List of tuples relative to nodes [string of the hex color,string of the name of the class]
                
                data_edges (list): A list of the following format, for each edge:
                    {'source': int, 'target': int, 'data': str, 'class': str}
                    
                    source: The id of the source node | Compulsory
                    
                    target: The id of the taget node | Compulsory
                    
                    data: String which gives some info about the edge | Optionnal, used when clicking on an edge to display info about it
                    
                    class: A string which gives the class of the given edge | Optionnal
                
                data_nodes (list): A list of the following format, for each node:
                    {'id': int, 'positionX': float, 'positionY': float, 'class': str, 'data': str, 'feature': list of float}
                
                    id: The local id of a node | Compulsory
                    
                    positionX, positionY : The position gave as input or compiled thanks to features | this is optional but nothing 
                        will appear if not provide.
                    
                    class: A string which gives the class of the given node | Optionnal
                    
                    feature: A list of float which give the embedding for a given node | Optionnal, not used for representation
                    
                    data: String which gives some info about the node | Optionnal, used when clicking on a node to display info about it
                    
            Instance variables :
                self.node_legend_map (dictionnary): Useful to map all the wrong node classification related to one class into one. 
                    At the end will have at most 3*Nb_class of node elements (normal/wrong/true)
                
                self.hash_node (dictionnary): Associate to every node id the selection status and the class associated
                
                self.hash_edge (dictionnary): Associate to every edge id the selection status and the class associated
                
                self.mask_edge (list): List of length the total edge number of boolean that change depending on which edge classes 
                    are selected/not selected
                
                self.mask_node (list): List of length the total node number of boolean that change depending on which edge classes 
                    are selected/not selected
                
                self.map (dictionnary): Map each node real id to the one gave in self.mask_node
                
                self.E (list of div): List of div of each edge class outputed in control panel
                
                self.N (list of div): List of div of each node class outputed in control panel

            Returns:
                Do not have any return arguments but apply changes to the instance of the CytoView class

            """
        self.data_edges=data_edges
        self.node_legend_map = {}
        # Allows to put all the different nodes type of wrong into one wrong button for each class and create the corresponding map
        for i in range(len(node_legend)):
            if "wrong" in node_legend[i][1]:
                real_class = node_legend[i][1].split(
                    "wrong_")[1].split('_sep_')[0]
                self.node_legend_map[node_legend[i][1]] = 'wrong_'+real_class
                node_legend[i][1] = "wrong_"+real_class

        node_legend = [list(x) for x in set(tuple(x) for x in node_legend)]

        self.hash_node = {}
        for elem in node_legend:
            self.hash_node[elem[1]] = {"selected": 1, "data": []}

        if self.hash_node != {}:
            for elem in data_nodes:
                if "wrong" in elem["class"]:
                    item = self.node_legend_map[elem["class"]]
                else:
                    item = elem["class"]
                self.hash_node[item]["data"] = self.hash_node[item]["data"]+[elem["id"]]

        self.hash_edge = {}
        for elem in edge_legend:
            self.hash_edge[elem[1]] = {"selected": 1, "data": []}

        if self.hash_edge != {}:
            c = 0
            for elem in data_edges:
                if "class" in elem:
                    self.hash_edge[elem["class"]
                                   ]["data"] = self.hash_edge[elem["class"]]["data"]+[c]
                    c += 1

        self.mask_edge = [1 for elem in data_edges]
        self.mask_node = [1 for elem in data_nodes]
        self.map = {data_nodes[i]['id']: i for i in range(len(data_nodes))}

        self.E = [html.Div(id={'class': 'edge_legend', 'index': edge_legend.index(elem), 'label': elem[1]},
                           children=[
            html.Div([html.P(elem[1], style={'text-overflow': 'ellipsis', 'font-size': '1.6vmin', 'margin': 'auto'})],
                     style={'width': '65%', 'height': '2em', 'display': 'inline-flex', 'align-items': 'center', 'text-align': 'center'}),
            html.Div(style={'width': '34%', 'height': '2em',
                     'display': 'inline-block', 'background-color': elem[0]})
        ]) for elem in edge_legend]


        self.N = [html.Div(id={'class': 'node_legend', 'index': node_legend.index(elem), 'label': elem[1]},
                           children=[
            html.Div([html.P(elem[1], style={'text-overflow': 'ellipsis', 'font-size': '1.6vmin', 'margin': 'auto'})],
                     style={'width': '65%', 'height': '2em', 'display': 'inline-flex', 'align-items': 'center', 'text-align': 'center'}),
            html.Div(style={'width': '34%', 'height': '2em',
                     'display': 'inline-block', 'background-color': elem[0]})
        ]) for elem in node_legend]

    def create_CP(self):
        r"""
            Creation of the Control Panel
            
            Args:

            Returns:
                html.Div: Div object composed of two tabs:
                    
                    Legend (dcc.Tab): A dcc.Tab object composed of three div objects:
                        
                        nodes-legend (div): A div component which take all the clickable nodes div in self.N
                            
                        edges-legend (div): A div component which take all the clickable nodes div in self.E
                            
                        clicked-element (div): An empty div component which will be filled when elements are clicked in the cytoscape view
                            
                    Export (dcc.Tab): A dcc.Tab object composed of three htlm.Button objects:
                        
                        btn-get-jpg (htlm.Button): Button for launching the download of the cytoscape view as jpg
                            
                        btn-get-png (htlm.Button): Button for launching the download of the cytoscape view as png
                            
                        btn-get-svg (htlm.Button): Button for launching the download of the cytoscape view as svg

            """

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
                                ], style={'background-color': '#F0F0F0', 'padding': '3%', 'margin': '4%'}
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
                                ], style={'background-color': '#F0F0F0', 'padding': '3%', 'margin': '4%'}
                            ),

                            html.Div(
                                children=[
                                    html.B(children='Clicked element'),
                                    html.Div(id='clicked-element',
                                             children=[]
                                             )
                                ], style={'background-color': '#F0F0F0', 'padding': '3%', 'margin': '4%'}
                            ),
                        ], style=self.styles['tab'])



                        ]),

                dcc.Tab(label='Export', children=[
                        html.Div(style=self.styles['tab'], children=[
                            html.Button("as jpg", id="btn-get-jpg"),
                            html.Button("as png", id="btn-get-png"),
                            html.Button("as svg", id="btn-get-svg")
                        ]
                        )
                        ])
            ]),


        ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top'})

    def get_callbacks(self, app):

        @app.callback(
            Output("cytoscape", "generateImage"),
            [
                Input("btn-get-jpg", "n_clicks"),
                Input("btn-get-png", "n_clicks"),
                Input("btn-get-svg", "n_clicks"),
            ])
        def get_image(get_jpg_clicks, get_png_clicks, get_svg_clicks):
            r"""
                Function that is launching the download of the actual representation of the cytoscape view
                
                Args:
                    get_jpg_clicks (int): Number of times the matched case was pressed
                        
                    get_png_clicks (int): Number of times the matched case was pressed
                    
                    get_svg_clicks (int): Number of times the matched case was pressed


                Returns:
                    dictionnary : Return a dictionnary to the cytoscape generate image component to precise in which format the file 
                        should be downloaded

                """

            # 'store': Stores the image data in 'imageData' !only jpg/png are supported
            # 'download'`: Downloads the image as a file with all data handling
            # 'both'`: Stores image data and downloads image as file.
            action = 'download'
            ftype = None
            ctx = dash.callback_context
            if ctx.triggered:
                input_id = ctx.triggered[0]["prop_id"].split(".")[0]
                # File type to output of 'svg, 'png', 'jpg', or 'jpeg' (alias of 'jpg')
                # ftype = input_id
                ftype = input_id.split("-")[-1]
                return {
                    'type': ftype,
                    'action': action
                }
            return dash.no_update

        # TODO : If we click rapidly on multiple links callbacks will be fired before the
        # one before had finished

        @app.callback(
            Output({"index": MATCH, "class": "edge_legend",
                   "label": MATCH}, "style"),
            Input({"index": MATCH, "class": "edge_legend",
                  "label": MATCH}, "n_clicks"),
        )
        def edge_selection(n):
            r"""
                Function that is changing the aspect of the MATCH edge button in the controlPanel when clicked on depending on whether it
                is selected or not. Furthemore this function is changing the mask_edge instance variable to remove or add edges of 
                the selected type (here index)
                
                Args:
                    n (int): Number of times the matched case was pressed
                        

                Returns:
                    dictionnary : Will be returned to the style component of the box corresponding to the Matched index in input
                        The only change is for opacity value wich is set to 0.2 if the edge are not selected (if the n value is odd)

                """
                
            triggered = dash.callback_context.triggered
            data_edge=self.data_edges
            if n is None:
                return {'height': '5vh', 'margin': "2%", 'display': 'flex', 'align-items': 'center'}

            elif n % 2 == 0:
                new_mask_edge = self.mask_edge
                for i in self.hash_edge[json.loads(triggered[0]['prop_id'].split('}',)[0]+'}')["label"]]["data"]:
                    if self.mask_node[self.map[data_edge[i]['source']]] == 1 and self.mask_node[self.map[data_edge[i]['target']]] == 1:
                        new_mask_edge[i] = 1
                self.hash_edge[json.loads(triggered[0]['prop_id'].split('}',)[
                                          0]+'}')["label"]]["selected"] = 1
                self.mask_edge = copy.deepcopy(new_mask_edge)
                return {'height': '5vh', 'margin': "2%", 'display': 'flex', 'align-items': 'center'}

            else:
                new_mask_edge = self.mask_edge
                for i in self.hash_edge[json.loads(triggered[0]['prop_id'].split('}',)[0]+'}')["label"]]["data"]:
                    new_mask_edge[i] = 0
                self.hash_edge[json.loads(triggered[0]['prop_id'].split('}',)[
                                          0]+'}')["label"]]["selected"] = 0
                self.mask_edge = copy.deepcopy(new_mask_edge)
                return {'height': '5vh', 'margin': "2%", 'display': 'flex', 'align-items': 'center', "opacity": "0.2"}

        # TODO : If we click rapidly on multiple links callbacks will be fired before the
        # one before had finished

        @app.callback(
            Output({"index": MATCH, "class": "node_legend",
                   "label": MATCH}, "style"),
            Input({"index": MATCH, "class": "node_legend",
                  "label": MATCH}, "n_clicks"),
        )
        def node_selction(n):
            r"""
                Function that is changing the aspect of the MATCH node button in the controlPanel when clicked on depending on whether it
                is selected or not. Furthemore this function is changing the mask_node instance variable to remove or add nodes of 
                the selected type (here index)
                
                Args:
                    n (int): Number of times the matched case was pressed
                        

                Returns:
                    dictionnary : Will be returned to the style component of the box corresponding to the Matched index in input
                        The only change is for opacity value wich is set to 0.2 if the edge are not selected (if the n value is odd)

                """
            data_edge=self.data_edges
            triggered = dash.callback_context.triggered

            if n is None:
                return {'height': '5vh', 'margin': "2%", 'display': 'flex', 'align-items': 'center'}
            elif n % 2 == 0:
                n_mask_node = self.mask_node
                n_mask_edge = self.mask_edge
                D = pd.DataFrame(data_edge)
                for i in self.hash_node[json.loads(triggered[0]['prop_id'].split('}',)[0]+'}')["label"]]["data"]:
                    n_mask_node[self.map[i]] = 1

                for i in self.hash_node[json.loads(triggered[0]['prop_id'].split('}',)[0]+'}')["label"]]["data"]:

                    for ind in D.index[D["target"] == i]:
                        if 'class' in D:
                            if self.hash_edge[D['class'].iloc[ind]]["selected"] == 1 and n_mask_node[self.map[D["source"][ind]]] == 1:

                                n_mask_edge[ind] = 1
                        else:
                            if n_mask_node[self.map[D["source"][ind]]] == 1:
                                n_mask_edge[ind] = 1

                    for ind in D.index[D["source"] == i]:
                        if 'class' in D:
                            if self.hash_edge[D['class'].iloc[ind]]["selected"] == 1 and n_mask_node[self.map[D["target"][ind]]] == 1:
                                n_mask_edge[ind] = 1
                        else:
                            if n_mask_node[self.map[D["target"][ind]]] == 1:
                                n_mask_edge[ind] = 1
                self.hash_node[json.loads(triggered[0]['prop_id'].split('}',)[
                                          0]+'}')["label"]]["selected"] = 1

                self.mask_node = copy.deepcopy(n_mask_node)
                self.mask_edge = copy.deepcopy(n_mask_edge)
                return {'height': '5vh', 'margin': "2%", 'display': 'flex', 'align-items': 'center'}

            else:
                n_mask_node = self.mask_node
                n_mask_edge = self.mask_edge
                D = pd.DataFrame(data_edge)
                for i in self.hash_node[json.loads(triggered[0]['prop_id'].split('}',)[0]+'}')["label"]]["data"]:
                    n_mask_node[self.map[i]] = 0
                    for ind in D.index[D["target"] == i]:
                        n_mask_edge[ind] = 0

                    for ind in D.index[D["source"] == i]:
                        n_mask_edge[ind] = 0

                self.hash_node[json.loads(triggered[0]['prop_id'].split('}',)[
                                          0]+'}')["label"]]["selected"] = 0
                self.mask_node = copy.deepcopy(n_mask_node)
                self.mask_edge = copy.deepcopy(n_mask_edge)
                return {'height': '5vh', 'margin': "2%", 'display': 'flex', 'align-items': 'center', "opacity": "0.2"}
