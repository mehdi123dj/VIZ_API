# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 09:55:01 2022

@author: remit
"""
import dash
import dash_bootstrap_components as dbc
from dash import html
import warnings

from CreateElements import CreateElements

    
# APP LAYOUT

 
app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
                external_stylesheets=[dbc.themes.LUX]
                )

app.title = 'Datarvest'
CE=CreateElements()
app.layout = html.Div(CE())

CE.get_callbacks(app)

if __name__ == '__main__':
    warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

    app.run_server(debug=True,use_reloader=False)
    # app.run_server(port=8050)


