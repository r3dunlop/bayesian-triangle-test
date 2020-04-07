import os
import dash
import dash_core_components as dcc
import dash_html_components as html

from util.stats import probability_of_x_differentiators, calculate_pvalue

app = dash.Dash(__name__)
server = app.server
colors = {
    'background' : '#111111',
    'text' : '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor' : colors['background']}, children=[
                      html.H1(
                          children = 'Number of discriminators',
                          style={
                              'textAlign' : 'center',
                              'color' : colors['text']
                          }
                      ),
                      html.Div(children='The probability of each discriminator', style={
                          'textAlign': 'center',
                          'color': colors['text']
                      }),
                      dcc.Graph(
                          id='Graph1',
                          figure={
                              'data': [
                                  {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                  {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                              ],
                              'layout': {
                                  'plot_bgcolor': colors['background'],
                                  'paper_bgcolor': colors['background'],
                                  'font': {
                                      'color': colors['text']
                                  }
                              }
                          }
                      )]
                )

if __name__ == '__main__':
    app.run_server(debug=True)