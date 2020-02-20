"""
Dash Tutorial Ch. 6 - example 3/

Stores output from an expensive processing step inside a hidden Div

Storing data inside a hidden Div is one of three main ways Dash supports
to make accessible across multiple Python processes.

"""

import time

from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = Dash(__name__)

df = pd.DataFrame([
    [1, 2],
    [2, 2],
    [4, 8], 
    [1, 9],
    [3, 7],
    [6, 2],

], columns=['x', 'y'])

graph = dcc.Graph(id='graph')
tbl = html.Table(id='table')

options = [
    {'label': i, 'value': df.iloc[i].x} for i in df.index
]
dropdown = dcc.Dropdown(id='dropdown', options=options)

hidden_div = html.Div(id='intermediate-value', style={'display': 'none'})

components = [graph, tbl, dropdown, hidden_div]

app.layout = html.Div(components)

@app.callback(
    Output('intermediate-value', 'children'),
    [Input('dropdown', 'value')]
)
def clean_data(value):
    # some expensive data processing step
    time.sleep(5)
    dff = df[df.index != value]
    return dff.to_json(orient='split')

def create_figure(df):
    data = [{
        'x': df.x,
        'y': df.y,
        'text': df.index,
        'mode': 'markers',
        'opacity': 0.7,
        'marker': {'size': 15, 'line': {'width': 0.5, 'color': 'white'}}
    }]

    layout = dict(
        xaxis={'title': 's', 'range':[0, 10]},
        yaxis={'title': 'y', 'range': [0, 10]},
        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest',
        transition={'duration': 500}
    )

    return {
        'data': data,
        'layout': layout
    }

@app.callback(
    Output('graph', 'figure'),
    [Input('intermediate-value', 'children')]
)
def update_graph(jsonified_data):
    dff = pd.read_json(jsonified_data, orient='split')

    figure = create_figure(dff)

    return figure

def create_table(df):
    return html.Table(
        [html.Tr(html.Th(col) for col in df.columns)] +
        
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(len(df))]
    )

@app.callback(
    Output('table', 'children'),
    [Input('intermediate-value', 'children')]
)
def update_table(jsonified_data):
    dff = pd.read_json(jsonified_data, orient='split')

    table = create_table(dff)
    
    return table

if __name__ == '__main__':
    app.run_server(debug=True)