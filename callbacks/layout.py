'''
Dash Tutorial Ch. 3 - example 1/5

Intro to callback functions. 

Callbacks let us dynamically update component properties based on changes to inputs. 

We might update: 
 * The children of a component to display new text
 * The figure of a dcc.Graph to display new data
 * The style of a component
 * Available options of a dcc.Dropdown component
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
])
"""
The @app.callback decorator is used to declare inputs and outputs to the app.

Inputs and outputs can be used as the properties of a component.

In this example, our input is the "value" property of the component with id='my-id', 
while the output is the "children" property of the component with id='my-div'.

Whenever an input property changes, the function that the callback decorator
wraps will be called automatically. Dash will pass the wrapped function with the new 
value of the input property as an input argument. Dash will update the property of the 
output component with whatever was returned by the function.

Callbacks are also called when the Dash app starts, passing any 
initial values of input components.
"""
@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You just typed: "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)