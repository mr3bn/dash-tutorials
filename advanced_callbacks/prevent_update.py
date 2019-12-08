'''
Dash Tutorial Ch. 4 - example 2/3

Demonstration of using PreventUpdate to selectively stop a callback function from firing
'''

import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

button = html.Button('Click here to see the secret', id='show-secret')

components = [button, html.Div(id='body-div')]

app.layout = html.Div(components)

@app.callback(
    Output(component_id='body-div', component_property='children'),
    [Input(component_id='show-secret', component_property='n_clicks')]
)
def update_output(n_clicks):
    # stop the callback function by raising a PreventUpdate exception
    if n_clicks is None:
        raise PreventUpdate
    else:
        return "Toss a little paprika on top, that's my secret!"

if __name__ == '__main__':
    app.run_server(debug=True)