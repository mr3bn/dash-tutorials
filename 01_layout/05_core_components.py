'''Introduction to the `dash_core_components` module.

The module includes a set of high-level components like dropdowns, 
graphs, markdown blocks, and more.

A gallery of available components is available at: 
https://dash.plot.ly/dash-core-components
'''

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

divs = []

options = [
    {'label': 'New York City', 'value': 'NYC'},
    {'label': u'Montréal', 'value': 'MTL'},
    {'label': 'San Francisco', 'value': 'SF'}
]

single_choice_dropdown = dcc.Dropdown(
    options=options,
    value='MTL'
)
divs +=[html.Label('Dropdown'), single_choice_dropdown]

multi_choice_dropdown = dcc.Dropdown(
    options=options,
    value=['MTL', 'SF'],
    multi=True
)
divs +=[html.Label('Multi-Select Dropdown'), multi_choice_dropdown]

radio = dcc.RadioItems(
    options=options,
    value='MTL'
)
divs +=[html.Label('Radio Items'), radio]

checklist = dcc.Checklist(
    options=options,
    value=['MTL', 'SF']
)
divs +=[html.Label('Checkboxes'), checklist]

text_input = dcc.Input(value='MTL', type='text')
divs +=[html.Label('Text Input'), text_input]

slider = dcc.Slider(
    min=0,
    max=9,
    marks={i: f'Label {1}' if i == 1 else str(i) for i in range(1, 6)},
    value=5
)
divs +=[html.Label('Slider'), slider]

app.layout = html.Div(
    divs,
    style={'columnCount': 2})

if __name__ == '__main__':
    app.run_server(debug=True)