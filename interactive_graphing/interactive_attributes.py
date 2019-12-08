"""
Dash Tutorial Ch. 5 - example 1/

Interactive graphs hello world. 

The dcc.Graph component has four attributes that chan change through user
interaction: hoverData, clickData, selectedData, and relayoutData. These properties 
update when you hover over, click on, or select regions of points in a graph.
"""

import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# four pairs of dummy points, two for each method of interactiviity
data = [
    {
        'x': [1, 2, 3, 4],
        'y': [4, 1, 3, 5],
        'text': ['a', 'b', 'c', 'd'],
        'customdata': ['c.a', 'c.b', 'c.c', 'c.d'],
        'name': 'Trace 1',
        'mode': 'markers',
        'marker': {'size': 12}
    }, 
    {
        'x': [1, 2, 3, 4],
        'y': [9, 4, 1, 4],
        'text': ['w', 'x', 'y', 'z'],
        'customdata': ['c.w', 'c.x', 'c.y', 'c.z'],
        'name': 'Trace 2',
        'mode': 'markers',
        'marker': {'size': 12}
    }
]

# toss the points on a basic graph
graph = dcc.Graph(
    id='basic-interactions',
    figure={
        'data': data,
        'layout': {
            'clickmode': 'event+select'
        }
    }
)

# text areas to display current values of interactive attributes
hover_text = html.Div([
    dcc.Markdown(d("""
        **Hover Data**
        
        Mouse over values in the graph.
    """)),
    html.Pre(id='hover-data', style=styles['pre'])
], className='three columns')

click_text = html.Div([
    dcc.Markdown(d("""
        **Click Data**
        
        Click on points in the graph.
    """)),
    html.Pre(id='click-data', style=styles['pre'])
], className='three columns')

selection_text = html.Div([
    dcc.Markdown(d("""
    **Selection Data**

    Choose the lasso or rectangle tool in the graph's menu
    bar and then select points in the graph.

    Note that if `layout.clickmode='event+select'`, selecton data
    accumulates (or un-accumulates) selected data if you hold down the
    `SHIFT` button while clicking.
    """)),
    html.Pre(id='selected-data', style=styles['pre'])
], className='three columns')

relayout_text = html.Div([
    dcc.Markdown(d("""
        **Zoom and Relayout Data**

        Click and drag on the graph to zoom or click on the zoom 
        buttons in the graph's menu bar.
        Clicking on legend items will also fire
        this event.
    """)),
    html.Pre(id='relayout-data', style=styles['pre']),
], className='three columns')

text_row = html.Div(
    className='row',
    children=[hover_text, click_text, selection_text, relayout_text]
)

components = [graph, text_row]

app.layout = html.Div(components)

"""
When supported interactions happen, attributes on the graph are updated automatically: 

 * Hover interactions update the hoverData attribute
 * Clicks update the clickData attribute
 * Selections update the selectedData attribute
 * Zooms or relayouots update the relayoutData attribute

These callback functions will pass upadated attribute values
to the text components underneath the graph.
"""

# updates the hover-data component with the value of the graph's hoverData attribute
@app.callback(
    Output('hover-data', 'children'),
    [Input('basic-interactions', 'hoverData')]
)
def display_hover_data(hover_data):
    return json.dumps(hover_data, indent=2)

# updates the click-data component with the value of the graph's clickData attribute
@app.callback(
    Output('click-data', 'children'),
    [Input('basic-interactions', 'clickData')]
)
def display_click_data(click_data):
    return json.dumps(click_data, indent=2)

# updates the selected-data component with the value of the graph's selectedData attribute
@app.callback(
    Output('selected-data', 'children'),
    [Input('basic-interactions', 'selectedData')]
)
def display_selected_data(selected_data):
    return json.dumps(selected_data, indent=2)

# updates the relayout-data component with the value of the graph's selectedData attribute
@app.callback(
    Output('relayout-data', 'children'),
    [Input('basic-interactions', 'relayoutData')]
)
def display_relayout_data(relayout_data):
    return json.dumps(relayout_data, indent=2)

if __name__ == '__main__':
    app.run_server(debug=True)