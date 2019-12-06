'''
Another example of callbacks, this time using a slider to update a graph.
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# create graph and slider components
graph = dcc.Graph(id='graph-with-slider')

slider = dcc.Slider(
    id='year-slider',
    min=df['year'].min(),
    max=df['year'].max(),
    value=df['year'].min(),
    marks={str(year): str(year) for year in df['year'].unique()},
    step=None
)

# put components into app layout
components = [graph, slider]
app.layout = html.Div(components)

# set up markers and a layout for the graph
marker = {
    'size': 15,
    'line': {'width': 0.5, 'color': 'white'}
}

# 
graph_layout = dict(
    xaxis={'type': 'log', 'title': 'GDP Per Capita', 'range':[2.3, 4.8]},
    yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    legend={'x': 0, 'y': 1},
    hovermode='closest',
    transition={'duration': 500}
)

# callback function to update the graph with changed values of the year slider
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    # use the slider value to slice the data
    filtered_df = df[df.year == selected_year]
    traces = []
    for c in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df.continent == c]
        traces.append(dict(
            x=df_by_continent.gdpPercap,
            y=df_by_continent.lifeExp,
            text=df_by_continent.country,
            mode='markers',
            opacity=0.7,
            marker=marker,
            name=c
        ))
    
    return {
        'data': traces,
        'layout': graph_layout
    }

if __name__ == '__main__':
    print({str(year): year for year in df.year.unique()})
    app.run_server(debug=True)