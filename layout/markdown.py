'''
Dash Tutorial Ch. 2 - example 5/6

Small example of driving content through Markdown. 

For larger blocks of text, we might prefer to write in Markdown instead. 

This example shows how to use Markdown content from a separate file 
by using the dcc.Markdown component.
'''

import markdown

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# read markdown from a separate file
text = open('text.md').read()

# plug markdown into a Div
app.layout = html.Div([
    dcc.Markdown(children=text)
])

if __name__ == '__main__':
    print('this example renders text from a markdown file in the browser')
    app.run_server(debug=True)