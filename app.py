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
                dcc.Dropdown(
                    id='dd-graph-type',
                    options=[
                        {'label': 'Number of Discriminators', 'value': 'NUMBER'},
                        {'label': 'Proportion of Discriminators', 'value': 'PROPORTION'},
                    ],
                    value='NUMBER',
                    clearable=False,
                    style=dict(
                        width='50%',
                    ),
                ) ,
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
                              'xaxis': {'title': 'Number of Discriminators', 'autorange': True},
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
               Input('input-correct','value'),
               Input('dd-graph-type','value')],
              [State('graph-probability-differentiators', 'figure'),
               State('graph-cumulative-probability-differentiators', 'figure')]
              )
def update_differentiator_graph(n, y, dd_val, pdf, cdf,):
    y = clean_integer(y)
    n = clean_integer(n)

    divisor = n
    mapping = ('number','proportion')
    if dd_val == 'NUMBER':
        divisor = 1
        mapping = ('proportion', 'number')


    pdf['data'] = [{'x': np.arange(0, n)/divisor, 'y': probability_of_x_differentiators(np.arange(0, n), y, n), 'type': 'bar',
               'name': 'Differentiators'}]

    cdf['data'] = [{'x': np.arange(0, n)/divisor, 'y': probability_of_more_than_x_differentiators(np.arange(0, n), y, n), 'type': 'bar',
         'name': 'Differentiators','marker':{ "color" : ['crimson']*n}},]

    for graph in [pdf,cdf]:
        graph['layout']['title'] = graph['layout']['title'].replace(*mapping)
        graph['layout']['title'] = graph['layout']['title'].replace(*map(lambda x: x.title(),mapping))
        graph['layout']['xaxis']['title']['text'] = graph['layout']['xaxis']['title']['text'].replace(*mapping)
        graph['layout']['xaxis']['title']['text'] = graph['layout']['xaxis']['title']['text'].replace(*map(lambda x: x.title(),mapping))

    return pdf, cdf

if __name__ == '__main__':
    app.run_server(debug=True)