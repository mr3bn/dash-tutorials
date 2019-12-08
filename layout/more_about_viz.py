'''
Dash Tutorial Ch. 2 - example 4/6

Introduction to the dash_core_components module. 

Demonstrates how to work with the primary dcc component, a Graph.
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# read dummy data from example
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

# get the data into a structure for plotly to take care of
marker = {
    'size':15,
    'line': {
        'width': 0.5, 'color': 'white'
    }
}

data = [{
    'x': df[df['continent'] == i]['gdp per capita'],
    'y': df[df['continent'] == i]['life expectancy'],
    'text': df[df['continent']==i].country,
    'mode': 'markers',
    'opacity': 0.7,
    'marker': marker,
    'name': i
} for i in df.continent.unique()]

# proviide a
layout = {
    'xaxis':{
        'type': 'log',
        'title': 'GDP Per Capita'
    },
    'yaxis': {
        'title': 'Life Expectancy'
    },
    'margin': {
        'l': 40, 
        'b': 40,
        't': 10,
        'r': 10
    },
    'legend': {'x': 0, 'y': 1},
    'hovermode': 'closest'
}

# the "figure" argument that dcc.Graph exposes is the same "figure" arg in plotly
# create one here by supplying the data & layout from above
fig = {
    'data': data,
    'layout': layout
}

# feed the figure into a dcc.Graph housed inside a Div
app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])

if __name__ == '__main__':
    print('this example prints a scatter plot of life expentency by GDP')
    print(df.head())
    app.run_server(debug=True)