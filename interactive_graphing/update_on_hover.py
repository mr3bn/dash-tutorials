"""
Dash Tutorial Ch. 5 - example 2/3

Reacting to "hover" events in a graph.

This application creates the same graph with configurable axes from 
the callbacks > multiple inputs example, and extends it by reacting
to hover events in the graph. When a single country point is hovered, 
time series graphs on the right of the screen will show the x- and y-axis 
indicators for that country over all time in the dataset.

"""

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = df['Indicator Name'].unique()

# crossfilter selectors
x_axis_column = dcc.Dropdown(
    id='crossfilter-xaxis-column',
    options=[{'label': i, 'value': i} for i in available_indicators],
    value='Fertility rate, total (births per woman)'
)

x_axis_type = dcc.RadioItems(
    id='crossfilter-xaxis-type',
    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
    value='Linear',
    labelStyle={'display': 'inline-block'}
)

y_axis_column = dcc.Dropdown(
    id='crossfilter-yaxis-column',
    options=[{'label': i, 'value': i} for i in available_indicators],
    value='Life expectancy at birth, total (years)'
)

y_axis_type = dcc.RadioItems(
    id='crossfilter-yaxis-type',
    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
    value='Linear',
    labelStyle={'display': 'inline-block'}
)

crossfilter_style = {'width': '49%', 'display': 'inline-block'}
container_style = {
    'borderBottom': 'thin lightgrey solid',
    'backgroundColor': 'rgb(250, 250, 250)',
    'padding': '10px 5px'
}

crossfilter_div = html.Div([
    html.Div([x_axis_column, x_axis_type], style=crossfilter_style),
    html.Div([y_axis_column, y_axis_type], style=crossfilter_style)
], style=container_style)


# scatter plot
scatter = dcc.Graph(
    id='crossfilter-indicator-scatter',
    hoverData={'points': [{'customdata': 'Japan'}]}
)

scatter_style = {'width': '49%', 'display': 'inline-block', 'padding': '0 20'}

scatter_div = html.Div([scatter], style=scatter_style)

# time series 
x_time_series = dcc.Graph(id='x-time-series')

y_time_series = dcc.Graph(id='y-time-series')

ts_style = crossfilter_style

ts_div = html.Div([x_time_series, y_time_series], style=ts_style)

# year slider
slider = dcc.Slider(
    id='crossfilter-year-slider',
    min=df['Year'].min(),
    max=df['Year'].max(),
    value=df['Year'].max(),
    marks={str(year): str(year) for year in df['Year'].unique()},
    step=None
)

slider_style = {'width': '49%', 'padding': '0px 20px 20px 20px'}

slider_div = html.Div(slider, style=slider_style)

components = [crossfilter_div, scatter_div, ts_div, slider_div]
app.layout = html.Div(components)

inputs = ['crossfilter-xaxis-column', 
    'crossfilter-yaxis-column', 
    'crossfilter-xaxis-type', 
    'crossfilter-yaxis-type', 
    'crossfilter-year-slider']

marker = {
    'size': 15,
    'opacity': 0.5,
    'line': {'width': 0.5, 'color': 'white'}
}

# same function as multi-input example from "Callbacks" chapter 
@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    [Input(i, 'value') for i in inputs]
)
def update_graph(x_axis_name, y_axis_name, x_axis_type, y_axis_type, year):
    dff = df[df['Year']==year]

    data = [dict(
        x=dff[dff['Indicator Name']==x_axis_name].Value,
        y=dff[dff['Indicator Name']==y_axis_name].Value,
        text=dff[dff['Indicator Name']==x_axis_name]['Country Name'],
        customdata=dff[dff['Indicator Name']==y_axis_name]['Country Name'],
        mode='markers',
        marker=marker
    )]

    layout = dict(
        xaxis={
            'title': x_axis_name,
            'type': x_axis_type.lower(),
        },
        yaxis={
            'title': y_axis_name,
            'type': y_axis_type.lower()
        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        height=450,
        hovermode='closest',
        transition={'duration': 500}
    )

    return {
        'data': data,
        'layout': layout
    }

# encapsulate logic to update both x- and y-axis time series
def create_time_series(dff, axis_type, title):
    
    data = [{
        'x': dff['Year'],
        'y': dff['Value'],
        'mode': 'lines+markers'
    }]
    
    layout = {
        'height': 225,
        'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
        'annotations': [{
            'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
            'xref': 'paper', 'yref': 'paper', 'showarrow': False,
            'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
            'text': title
        }],
        'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
        'xaxis': {'showgrid': False}
    }

    return {
        'data': data,
        'layout': layout
    }

# update the x-axis time series on hover in the main graph
@app.callback(
    Output('x-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value')]
)
def update_x_timeseries(hoverData, axis_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == axis_name]
    title = f'<b>{country_name}</b><br>{axis_name}'
    return create_time_series(dff, axis_type, title)

# update the y-axis time series on hover in the main graph
@app.callback(
    Output('y-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value')]
)
def update_y_timeseries(hoverData, axis_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name']==country_name]
    dff = dff[dff['Indicator Name'] == axis_name]
    title = f'<b>{country_name}</b><br>{axis_name}'
    return create_time_series(dff, axis_type, title)

if __name__ == '__main__':
    app.run_server(debug=True)