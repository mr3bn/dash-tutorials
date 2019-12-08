'''
Dash Tutorial Ch. 4 - example 3/3

Demonstrates how to use no_update to handle bad inputs while showing the previous one.
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

paragraph = 'Enter a composite number to see its prime factors'
num_input = dcc.Input(id='num', type='number', debounce=True, min=1, step=1)
error = html.P(id='err', style={'color':'red'})
output = html.P(id='out')

components = [paragraph, num_input, error, output]
app.layout = html.Div(components)

@app.callback(
    [Output('out', 'children'), Output('err', 'children')],
    [Input('num', 'value')]
)
def show_factors(num):
    if num is None:
        # PreventUpdate prevents ALL outputs from updating
        raise dash.exceptions.PreventUpdate

    factors = prime_factors(num)

    if len(factors) == 1:
        # dash.no_update prevents any single ouotput from updating
        return dash.no_update, '{} is prime!'.format(num)

    return '{} is {}'.format(num, ' * '.join(str(n) for n in factors)), ''


def prime_factors(num):
    n, i, out = num, 2, []
    while i * i <= n:
        if n % i == 0:
            n = int(n / i)
            out.append(i)
        else:
            i += 1 if i == 2 else 2
    out.append(n)
    return out


if __name__ == '__main__':
    app.run_server(debug=True)