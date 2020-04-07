import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import numpy as np
from util.stats import probability_of_x_differentiators, calculate_pvalue

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
                html.H1(
                    children='Number of discriminators',
                ),
                html.H3(children='The probability of number of discriminators',),
                html.Div([
                    html.Div([
                        'Number of Tasters: ',
                        dcc.Input(id='input-tasters', type='number', value='24'),
                    ],
                        style=dict(
                            width='30%',
                        ),
                    ),
                    html.Div([
                        'Number of Correct: ',
                        dcc.Input(id='input-correct', type='number', value='12'),
                    ],
                        style=dict(
                            width='30%',
                        ),
                    ),
                ]),
                dcc.Graph(
                      id='graph-probability-differentiators',
                      figure={
                          'data': [
                              {'x': np.arange(0,24), 'y': probability_of_x_differentiators(np.arange(0,24),12,24), 'type': 'bar', 'name': 'Differentiators'},
                          ],



                      }
                  )]
            )

@app.callback(Output('graph-probability-differentiators', 'figure'),
              [Input('input-tasters', 'value'),
               Input('input-correct','value')])
def update_differentiator_graph(n, y):
    y = int(y)
    n = int(n)
    return {'data': [{'x': np.arange(0,n), 'y': probability_of_x_differentiators(np.arange(0,n),y,n), 'type': 'bar', 'name': 'Differentiators'},]}


if __name__ == '__main__':
    app.run_server(debug=True)