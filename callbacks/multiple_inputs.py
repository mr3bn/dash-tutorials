'''
Dash Tutorial Ch. 3 - example 3/5

Demonstration of binding multiple inputs to one output in a callback.

Creates five input components that manipulate different aspects of a graph,
and uses a callback function to update the graph whenever the value of an 
input component is changed.
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = df['Indicator Name'].unique()

x_axis_column_name = dcc.Dropdown(
    id='xaxis-column',
    options=[{'label': i, 'value': i} for i in available_indicators],
    value='Fertility rate, total (births per woman)'
)

x_axis_type = dcc.RadioItems(
    id='xaxis-type',
    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
    value='Linear',
    labelStyle={'display': 'inline-block'}
)

y_axis_column_name = dcc.Dropdown(
    id='yaxis-column',
    options=[{'label': i, 'value': i} for i in available_indicators],
    value='Life expectancy at birth, total (years)'
)

y_axis_type = dcc.RadioItems(
    id='yaxis-type',
    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
    value='Linear',
    labelStyle={'display': 'inline-block'}
)

x_axis_options = [x_axis_column_name, x_axis_type]
x_div = html.Div(x_axis_options, style={'width': '48%', 'display': 'inline-block'}),

y_axis_options = [y_axis_column_name, y_axis_type]
y_div = html.Div(y_axis_options, style={'width': '48%', 'display': 'inline-block'})

axis_options = html.Div([x_div, y_div])

graph = dcc.Graph(id='indicator-graphic')

slider = dcc.Slider(
    id='year-slider',
    min=df['Year'].min(),
    max=df['Year'].max(),
    value=df['Year'].max(),
    marks={str(year): str(year) for year in df['Year'].unique()},
    step=None
)

app.layout = html.Div([
    html.Div([
        html.Div([
            x_axis_column_name,
            x_axis_type
        ], style={'width': '48%', 'display': 'inline-block'}),
    
        html.Div([
            y_axis_column_name,
            y_axis_type
        ], style={'width': '48%', 'display': 'inline-block'})
    ]),
    graph,
    slider
])

# graph details
graph_marker={
    'size': 15,
    'opacity': 0.5,
    'line': {'width': 0.5, 'color': 'white'}
}

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('year-slider', 'value')]
)
def update_graph(x_column_name, y_column_name, x_axis_type, y_axis_type, year):
    dff = df[df['Year'] == year]

    data = [dict(
        x=dff[dff['Indicator Name'] == x_column_name]['Value'],
        y=dff[dff['Indicator Name'] == y_column_name]['Value'],
        text=dff[dff['Indicator Name'] == y_column_name]['Country Name'],
        mode='markers',
        marker=graph_marker
    )]

    layout = dict(
        xaxis={
            'title': x_column_name,
            'type': x_axis_type.lower(),
        },
        yaxis={
            'title': y_column_name,
            'type': y_axis_type.lower()
        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest',
        transition={'duration': 500}
    )


    return {
        'data': data, 
        'layout': layout
    }

if __name__ == '__main__':
    app.run_server(debug=True)