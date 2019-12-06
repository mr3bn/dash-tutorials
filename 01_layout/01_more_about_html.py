'''
Examples of basic items in dash_html_components.

The dash_html_components module contains a class for
every HTML tag as well as keyword args for all HTML arguments.
'''

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

elements = []

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# html H1 tag
title = html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    )

elements += [title]

# html div tag
subtitle = html.Div(children='Dash: A web application framework for Python.', style={
    'textAlign': 'center',
    'color': colors['text']
    })

elements += [subtitle]

# throw a graph in for good measure
graph = dcc.Graph(
    id='example-graph-2',
    figure={
        'data': [
            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        ],
        'layout': {
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            }
        }
    }
)

elements += [graph]

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, 
    children=elements
)

if __name__ == '__main__':
    app.run_server(debug=True)