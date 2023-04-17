import dash
from dash import html
import plotly.graph_objects as go
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np

from utils import *
from graphing_utils import *
from text_utils import *

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

app.title = "Data Anomaly Judgement Dashboard"

server = app.server

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

mc_row_index = 0
kp_row_index = 0

platform = '温商贷'

plat_df = get_platform_df(platform)


navbar = dbc.Navbar(id='navbar', children=[
    dbc.Row([
        dbc.Col(html.Img(src=PLOTLY_LOGO, height="10px")),
        dbc.Col(
            dbc.NavbarBrand("Data Anomaly Judgement Dashboard", style={'color': 'white', 'fontSize': '20px', 'fontFamily': 'Times New Roman'}
                            )
        )
    ], align="center", style={'height': '20px'}
    ),
], color='#0F3680')

button_style = {
    # Set the background color with opacity
    'background-color': 'rgba(211, 211, 211, 0.7)',
    'border': '2px solid #808080',  # Add a border with a gray color
    'color': 'black',  # Set the font color to white
    'padding': '5px 20px',  # Set the button padding
    'text-align': 'center',  # Center the button text
    'text-decoration': 'none',  # Remove the underline on the button text
    'display': 'inline-block',  # Set the display property
    'font-size': '16px',  # Set the font size
    'border-radius': '5px',  # Round the button edges
    'cursor': 'pointer',  # Change the cursor to a pointer on hover
    'transition-duration': '0.4s',  # Add a transition effect on hover
}

app.layout = html.Div([
    navbar,
    dbc.Container([
        dbc.Row([

            html.Div([
                dcc.Dropdown(
                    [1, 2, 3],
                    'Fertility rate, total (births per woman)',
                    id='crossfilter-xaxis-column',
                    style={'margin-top': '10px'}
                ),
                dcc.Dropdown(
                    [1, 2, 3],
                    'Fertility rate, total (births per woman)',
                    id='crossfilter-xaxis-column2',
                    style={'margin-top': '10px'}
                ),
                dash.dash_table.DataTable(
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'lineHeight': '15px'
                    },
                    css=[{
                        'selector': '.dash-spreadsheet td div',
                                    'rule': '''
                                                    line-height: 15px;
                                                    max-height: 30px; min-height: 30px; height: 30px;
                                                    display: block;
                                                    overflow-y: hidden;
                                                    
                                                '''
                    }],
                    data=plat_df.to_dict('records'),
                    columns=[{"name": i, "id": i}
                             for i in plat_df.columns],
                    # fixed_columns={'headers': True, 'data': 1},
                    style_cell_conditional=[
                        {'if': {'column_id': '知识词典'},
                         'width': '100%'},
                    ],
                    # style_cell={
                    #         'overflow': 'hidden',
                    #         'textOverflow': 'ellipsis',
                    #         'maxWidth': 0
                    #     },
                    page_size=10,
                    style_table={
                        'height': '400px',
                        'overflowX': 'auto',
                        'margin-top': '10px'
                    },
                    id='tbl'
                )
            ], style={'width': '17%', 'float': 'right', 'display': 'inline-block',
                      'position': 'absolute',
                      'left': '20px'
                      }),

            dbc.Col(
                dbc.Tabs([
                    dbc.Tab(dcc.Graph(
                        id='daily-figure',
                        figure=plot_combined(platform)
                    ),
                        label='Average Daily Temp', style={'position': 'relative', 'left': '0px', 'width': '58%'}
                    ),
                    dbc.Tab([
                        dcc.Dropdown(
                            [1, 2, 3],
                            'Fertility rate, total (births per woman)',
                            id='crossfilter-xaxis-column1',
                            style={'position': 'relative',
                                               'left': '60%', 'width': '50%'}
                        ),
                        dcc.Graph(
                            id='high-low-figure',
                            figure=plot_feature_trend(
                                platform, 'TradingVolume')
                        )
                    ],
                        label="Daily Highs and Lows", style={'position': 'relative', 'left': '0px', 'width': '58%', 'height': '90%'}),
                    dbc.Tab(dcc.Graph(
                        id='weekly-figure',
                        figure=plot_static_data()
                    ),
                        label="Last Seven Days", style={'position': 'relative', 'left': '0px', 'width': '58%'}
                    )
                ], style={'position': 'relative', 'left': '0px', 'width': '58%'}
                ), style={'position': 'relative', 'left': '14%', 'width': '60%'}
            ),

            html.Div([

                dbc.Row(
                    dbc.Col(
                        html.Div([
                            html.H5(platform+" — 平台基本信息",
                                    id='current-temp4'),
                            dcc.Markdown(
                                f"""
                                        {get_basic_info_text(platform)}
                                        """, style={'line-height': '0.8', "margin-top": "20px", "margin-bottom": "20px", "overflow": "scroll", }
                            )
                        ], style={
                            "width": "230px",
                            "height": "280px",
                            "margin-left": "20px",
                            "margin-top": "20px",
                            # "border": "1px solid black",
                            "border-bottom": "1px solid gray",
                            "padding": "10px",
                            "overflow": "auto",
                        },
                        )
                    )),

                dbc.Row(
                    dbc.Col([
                        html.Div([
                            html.H5("毛刺信息", id='current-temp6'),
                            dcc.Markdown(
                                f"""
                                        {get_mc_info_text(mc_row_index)}
                                        """, style={'line-height': '1.2', "margin-top": "20px", "margin-bottom": "20px", "overflow": "scroll"}
                            )
                        ], style={
                            "width": "230px",
                            "height": "250px",
                            "margin-left": "20px",
                            "margin-top": "20px",
                            "margin-bottom": "20px",
                            # "border-bottom": "1px solid gray",
                            # "border": "1px solid black",
                            "padding": "10px",
                            "overflow": "auto",
                        },
                        )
                    ])),


            ], style={'width': '16%', 'float': 'right', 'display': 'inline-block', 'position': 'absolute', 'right': '50px'})
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Markdown(
                        f"""
                                    {get_kp_info_text(plat_df, kp_row_index)}
                                    """, style={'line-height': '1.2', "margin-top": "20px", "margin-bottom": "20px", "overflow": "scroll"}
                    )
                ], style={
                    "width": "230px",
                    "height": "180px",
                    # "margin-left" : "20px",
                    # "margin-bottom" : "20px",
                    "border-top": "1px solid gray",
                    # "border": "1px solid black",
                    "padding": "0px",
                    "overflow": "auto",
                },
                )
            ], width=2, style={'position': 'absolute', 'left': '20px'}),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col(
                                html.H4("是否判断为数据毛刺?"), style={'margin-left': '20px', 'margin-top': '10px'}),
                            dbc.Col(
                                dcc.RadioItems(
                                    options=[
                                        {'label': '是', 'value': 'yes'},
                                        {'label': '否', 'value': 'no'},
                                        {'label': '不确定',
                                         'value': 'not_sure'}
                                    ],
                                    labelStyle={'display': 'inline-block',
                                                'margin-left': '20px', 'margin-right': '40px',
                                                'margin-top': '0px',
                                                'transform': 'scale(1.5)'
                                                },
                                    id='radio-items', className='align-items-start', style={'margin-left': '20px', 'margin-top': '10px'}
                                )
                            ),
                        ])
                    ]),
                    dbc.CardBody(
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    # html.Br(),
                                    dbc.Input(
                                        placeholder='Reason',
                                        type='text',
                                        id='reason-input',
                                        style={
                                            'width': '100%', 'margin-top': '0px', 'margin-left': '20px'}
                                    ),
                                    # html.Br(),
                                    dbc.Input(
                                        placeholder='Remarks',
                                        type='text',
                                        id='remarks-input',
                                        style={
                                            'width': '100%', 'margin-top': '10px', 'margin-left': '20px'}
                                    )
                                ], width=9),
                                dbc.Col([
                                    html.Div([
                                        html.Button('OK', id='ok-button', n_clicks=0, style={
                                            **button_style, 'margin-top': '0px', 'margin-left': '30px'}),
                                        html.Button('Submit', id='submit-button', n_clicks=0, style={
                                            **button_style, 'margin-top': '10px', 'margin-left': '30px'}, className='btn-submit'),
                                    ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'flex-end', 'margin-top': '0px'}),
                                ], width=3, style={'text-align': 'right', 'justify-content': 'flex-end'})
                            ], className='mt-3')
                        ])
                    ),
                    # dbc.CardFooter(id = 'low-temp-date2')
                ],
                    color="white",
                    style={'left': '14%', 'width': '72%', 'height': '200px'})],
            ),
            dbc.Col([
                html.Div([
                    html.Button('Previous', id='previous-button', n_clicks=0,
                                style={**button_style, 'margin-top': '30px'}),
                    html.Button('Next', id='next-button', n_clicks=0,
                                style={**button_style, 'margin-top': '10px'}),
                    html.Button('Save and Quit', id='save-quit-button',
                                n_clicks=0, style={**button_style, 'margin-top': '10px'}),
                ], style={'display': 'flex', 'flex-direction': 'column', "border-top": "1px solid gray", "margin-top": "20px"})
            ], width=2,
                style={'position': 'absolute', 'right': '20px'})
        ],

            justify="center", style={
            # "margin-top": "2rem",
            'margin': '0px'}
        )
    ]
    ),
]
)

# ## Daily Average Figure
# @app.callback(Output('daily-figure', 'figure'),
#               Input('interval-component', 'n_intervals'))
# def update_daily_averages(n):
#     return daily_fig


# --------------------- CallBacks -------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
