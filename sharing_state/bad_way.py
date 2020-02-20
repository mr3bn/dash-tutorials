"""
Dash Tutorial Ch. 6 - example 1/

Sketch example of the WRONG WAY to modity data out of scope. 

This pattern *WILL NOT WORK RELIABLY* because Dash is designed to 
work in multi-user environments. If an app uses modified globals, 
then one user's session can affect another's. Not great!

Additionally, Dash is designed to be run with multiple workers so that
callbacks can be executed in parallel. Workers do NOT share memory, so 
if one worker modifies a global variable then that modification will
not be applied to the other worker processes.

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
    # do not do this -- updating globals out of scope is not safe!!!
    global df 
    df = df[df['c'] == value]
    return len(df)