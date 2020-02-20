"""
Dash Tutorial Ch. 6 - example 2/

Sketch example of the RIGHT WAY to modity data out of scope. 

Fixes the example in "bad_way.py" by re-assigning the out-of-scope
data to a new variable inside the callback's scope.

"""

from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = Dash(__name__)

df = pd.DataFrame([
    [1, 2, 3],
    [4, 1, 4], 
    ['x', 'y', 'z']
], columns=['a', 'b', 'c'])

dropdown = dcc.Dropdown(
    id='dropdown',
    options=[{'label': i, 'value': i} for i in df.c.unique()],
    value='a'
)

output = html.Div(id='output')

components = [dropdown, output]

app.layout = html.Div(components)

@app.callback(
    Output('output', 'children'),
    [Input('dropdown', 'value')])
def update_output_bad(value): 
    # the right way to work with out-of-scope data: assign a new name
    filtered_df = df[df['c'] == value]
    return len(filtered_df)