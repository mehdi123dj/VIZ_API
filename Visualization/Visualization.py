# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 09:55:01 2022

@author: remit
"""
import dash
import dash_bootstrap_components as dbc
from dash import html
import warnings
import flask
from CreateElements import CreateElements

# To use to declare the flask server (it is really useful for gunicorn use)
server = flask.Flask(__name__)




app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport",
                            "content": "width=device-width, initial-scale=1"}],
                external_stylesheets=[dbc.themes.LUX],
                suppress_callback_exceptions=True,
                server=server
                )

app.title = 'Datarvest'

# Initialize Create Elements class
CE = CreateElements()

# APP LAYOUT
app.layout = html.Div(CE())

# Take all the callbacks of the class that are inside CreateElements
CE.get_callbacks(app)

if __name__ == '__main__':
    warnings.filterwarnings(
        action="ignore", message="unclosed", category=ResourceWarning)

    # app.run(debug=True,use_reloader=False)
    app.run(host="0.0.0.0", port=8050)
