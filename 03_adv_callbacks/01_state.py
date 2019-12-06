'''
Demonstrates the usage of State, which allows component values used in callbacks
to be modified without firing the callback function.
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

input_1 = dcc.Input(id='input-1-state', type='text', value='Montréal')
input_2 = dcc.Input(id='input-2-state', type='text', value='Canada')
submit_button = html.Button(id='submit-button', n_clicks=0, children='Submit')

components = [input_1, input_2, submit_button, html.Div(id="output-state")]
app.layout = html.Div(components)

@app.callback(
    Output('output-state', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-1-state', 'value'), 
    State('input-2-state', 'value')],
)
def update_output(n_clicks, input_1, input_2):
    return u'''
    The button has been pressed {} times,
    Input 1 is "{}",
    and Input 2 is "{}"
    '''.format(n_clicks, input_1, input_2)


if __name__ == "__main__":
    app.run_server(debug=True)