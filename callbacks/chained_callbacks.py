"""
Dash Tutorial Ch. 3 - example 5/5

Example of chaining two Dash callback functions.

This pattern can be used to create dynamic UIs where one input
component updates some prooperty of another.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montréal', 'Toronto', 'Ottawa']
}

countries = dcc.RadioItems(
    id='countries-radio',
    options=[{'label': k, 'value': k} for k in all_options.keys()],
    value='America'
)

cities = dcc.RadioItems(id='cities-radio')

components = [
    countries,
    html.Hr(),
    cities,
    html.Hr(),
    html.Div(id='display-selected-values')
]

app.layout = html.Div(components)

# this callback dynamically populates the "cities" radio list based on the country selection
@app.callback(
    Output('cities-radio', 'options'),
    [Input('countries-radio', 'value')]
)
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

# this callback populates the plaiintext div when a selection is made
# in either city or country radio lists
@app.callback(
    Output('display-selected-values', 'children'),
    [Input('countries-radio', 'value'),
    Input('cities-radio', 'value')]
)
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(selected_city, selected_country)


if __name__ == '__main__':
    app.run_server(debug=True)