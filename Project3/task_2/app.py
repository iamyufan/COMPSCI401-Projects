from dash import Dash, html, dcc
import plotly.express as pxr
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import redis
import json
from dash.dependencies import Input, Output
r = redis.Redis(host='152.3.65.126', port=6379, db=0)
app = Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H5(children='💙COMPSCI 401-Cloud Computing: Project 3 (Yufan Zhang)💚', 
        style={'textAlign': 'center','fontSize':'15px'}),
        html.Div(id='live-update-text'),
        # dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    r = redis.Redis(host = '152.3.65.126', port=6379, db=0)
    metrics = r.get('yz605-proj3-output')
    metrics = json.loads(metrics.decode("utf-8"))
    return [html.Div(
            children = [
                html.H1(children = "Resource Usage Monitor",
                        style = {"textAlign": "center"}
                    ),        
                html.Div(children = "Avg Utilization of CPUs and Virtual Memory (%)",
                        style = {"textAlign": "center"}
                    ),
                dcc.Graph(id = "graph-2",
                        figure = {'data':[{'x': ['CPU 0', 'CPU 1', 'CPU 2', 'CPU 3'], 'y':[metrics[f'avg-cpu_percent-{i}-60sec'] for i in range(4)], 'type': 'bar', 'name': 'over the last minute'},
                                        {'x': ['CPU 0', 'CPU 1', 'CPU 2', 'CPU 3'], 'y':[metrics[f'avg-cpu_percent-{i}-1hour'] for i in range(4)], 'type': 'bar', 'name': 'over the last hour'},
                                        {'x': ['Vertual Memory'], 'y':[metrics['avg-virtual_memory-60sec']], 'type': 'bar', 'name': 'over the last minute'}
                                    ]
                            }
                    ),
                html.Span(metrics['timestamp']), html.Br(), html.Br(),
                html.Table(
                    style={'textAlign':'center','width':'800px','height':'128px'},
                    className='formCenter',
                    children=[
                        html.Thead(
                            html.Tr([
                                html.Th('CPU ID'),html.Th('Avg utilization over the last minute minute (%)'),
                                html.Th('Avg utilization over the last hour (%)')
                                ])
                        ),
                        html.Tbody([
                            html.Tr([
                                html.Td(i),
                                html.Td(metrics[f'avg-cpu_percent-{i}-60sec']),
                                html.Td(metrics[f'avg-cpu_percent-{i}-1hour'])
                                ]) for i in range(4)
                    ]),  
                ]),html.Br(),
                html.Span('Average memory utilization over the last min(%): '+str(metrics['avg-virtual_memory-60sec']), style={'textAlign': 'center','fontSize':'15px'}),
            ])
        ]
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=5116)
    