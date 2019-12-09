"""
Dash Tutorial Ch. 5 - example 3/3

Generic example of crossfiltering across a high-dimensional dataset. 

This app produces three scatter plots and, through a callback, will propagate
a selection on one chart to the other two.
"""

from pprint import pprint

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# create a six-column dataset to plot across three scatter charts
np.random.seed(0)
df = pd.DataFrame({f"Col {i+1}" : np.random.rand(30) for i in range(6)})


graph_config = {'displayModeBar': False}

# three empty graphs - the callback will handle plotting data on them
g1 = dcc.Graph(id='g1', config=graph_config)
g2 = dcc.Graph(id='g2', config=graph_config)
g3 = dcc.Graph(id='g3', config=graph_config)

graphs = (g1, g2, g3)

components = [html.Div(g, className='four columns') for g in graphs]

app.layout = html.Div(components)

def get_figure(df, x_col, y_col, selected_points, local_selection):
    """
    Updates selections in a scatter plot based on an input selection
    and the current state of selected data in the plot.
    """
    
    # if there is a local selection, find its bounds so we can persist a rectangle
    if local_selection and local_selection['range']:
        pprint(f'local_selection: {local_selection}')
        ranges = local_selection['range']
        selection_bounds = {
            'x0': ranges.get('x')[0], 'x1': ranges.get('x')[1],
            'y0': ranges.get('y')[1], 'y1': ranges.get('y')[1]
        }
    # otherwise set the bounds as the whole chart area
    else:
        selection_bounds = {
            'x0': np.min(df[x_col]), 'x1': np.max(df[x_col]),
            'y0': np.min(df[y_col]), 'y1': np.max(df[y_col])
        }

    data = [dict(
        x=df[x_col],
        y=df[y_col],
        text=df.index,
        textposition='top',
        selectedpoints=selected_points,
        customdata=df.index,
        type='scatter',
        mode='markers+text',
        marker={'color': 'rgba(0, 116, 217, 0.7)', 'size': 12},
        unselected={
            'marker': {'opacity': 0.3},
            'textfont': {'color': 'rbga(0, 0, 0, 0)'}
        }
    )]

    layout = {
        'margin': {'l': 20, 'r': 0, 'b': 15, 't': 5},
        'dragmode': 'select',
        'hovermode': False,
        # Display a rectangle to cover the selection bounds
        'shapes': [dict({
            'type': 'rect',
            'line': { 'width': 1, 'dash': 'dot', 'color': 'darkgrey' }
        }, **selection_bounds
        )]
    }

    return {
        'data': data,
        'layout': layout
    }

@app.callback(
    [Output(g.id, 'figure') for g in graphs],
    [Input(g.id, 'selectedData') for g in graphs]
)
def callback(selection1, selection2, selection3):
    """
    Update all three graphs whenever the selected points on any graph changes.

    Takes the local selection from the graph that was changed, finds all points
    contained within it, and calls get_figure() to update the other graphs to 
    reflect the same selection.
    """
    
    selected_points = df.index

    for selected_data in [selection1, selection2, selection3]:
        if selected_data and selected_data.get('points'):
            # if there are points selected in any graph, 
            selected_points = np.intersect1d(
                selected_points, 
                [p.get('customdata') for p in selected_data.get('points')]
            )
    
    return [get_figure(df, "Col 1", "Col 2", selected_points, selection1),
            get_figure(df, "Col 3", "Col 4", selected_points, selection2),
            get_figure(df, "Col 5", "Col 6", selected_points, selection3)]

if __name__ == '__main__':
    app.run_server(debug=True)