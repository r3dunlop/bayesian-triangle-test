import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import numpy as np
from util.stats import probability_of_x_differentiators, probability_of_more_than_x_differentiators, calculate_pvalue

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
                        dcc.Input(id='input-tasters', type='number', value='24', placeholder='1'),
                    ],
                        style=dict(
                            width='30%',
                        ),
                    ),
                    html.Div([
                        'Number of Correct: ',
                        dcc.Input(id='input-correct', type='number', value='12', placeholder='1'),
                    ],
                        style=dict(
                            width='30%',
                        ),
                    ),
                ]),
                html.H3('p-value: ',id='pvalue'),
                dcc.Graph(
                      id='graph-probability-differentiators',
          #            animate= True,
                      figure={
                          'data': [
                              {'x': np.arange(0,24), 'y': probability_of_x_differentiators(np.arange(0,24),12,24), 'type': 'bar', 'name': 'Differentiators'},
                          ],
                          'layout': {
                              'title': 'Probability of the number of discriminators',
                              'yaxis': {'title': 'Probability', 'autorange': True},
                              'xaxis': {'title': 'Number of Differentiators', 'autorange': True},
                              'bargap':0,

                          }

                      },

                  ),
                dcc.Graph(
                    id='graph-cumulative-probability-differentiators',
                #    animate=True,
                    figure={
                        'data': [
                            {'x': np.arange(0, 24), 'y': probability_of_x_differentiators(np.arange(0, 24), 12, 24), 'type': 'bar',
                             'name': 'Differentiators', 'marker' : { "color" : ['crimson']*24}},
                        ],
                        'layout': {
                            'title': 'Probability of more than x number of differentiators',
                            'yaxis': {'title': 'Probability', 'autorange': True},
                            'xaxis': {'title': 'Number of Differentiators', 'autorange': True},
                            'bargap': 0,

                        }

                    },

                )

                ]
            )

def clean_integer(i):
    if i is None:
        return 1
    return int(i)

@app.callback(Output('pvalue', 'children'),
              [Input('input-tasters', 'value'),
               Input('input-correct','value')])
def update_pvalue(n, y):
    y = clean_integer(y)
    n = clean_integer(n)
    return 'p-value: {}'.format(round(calculate_pvalue(y,n),3))

@app.callback([Output('graph-probability-differentiators', 'figure'),
               Output('graph-cumulative-probability-differentiators', 'figure')],
              [Input('input-tasters', 'value'),
               Input('input-correct','value')],
              [State('graph-probability-differentiators', 'figure'),
               State('graph-cumulative-probability-differentiators', 'figure')]
              )
def update_differentiator_graph(n, y, pdf, cdf):
    y = clean_integer(y)
    n = clean_integer(n)
    pdf['data'] = [{'x': np.arange(0, n), 'y': probability_of_x_differentiators(np.arange(0, n), y, n), 'type': 'bar',
               'name': 'Differentiators'}]
    cdf['data'] = [{'x': np.arange(0, n), 'y': probability_of_more_than_x_differentiators(np.arange(0, n), y, n), 'type': 'bar',
         'name': 'Differentiators','marker':{ "color" : ['crimson']*n}},]
    return pdf, cdf

if __name__ == '__main__':
    app.run_server(debug=True)