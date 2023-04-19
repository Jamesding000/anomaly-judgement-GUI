import dash
from dash import html
import plotly.graph_objects as go
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import time
import sys

from graphing_utils import *
from data_processing_utils import *
from CLASS_LIST import *

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

app.title = "Data Anomaly Judgement Dashboard"

server = app.server

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
MIN_MC_ROW_INDEX = 0
MAX_MC_ROW_INDEX = 9612
KP_TABLE_PAGE_SIZE = 10
TF_COL_INDEX = 7
REASON_COL_INDEX = 9
REVISE_COL_INDEX = 10
    

mc_row_index = get_curr_line_no()

# load in all the checked mc information
checked_mc_info_dict = checked_mc_df_to_dict()
kp_row_index = 0

row = mc_df.iloc[mc_row_index]
plat, mc_feature, mc_x, mc_y = row['平台'], row['时间序列名称'], row['日期'], row['数值']

# print([plat, mc_feature, mc_x, mc_y])

# initial setup
kp_df = get_platform_df(plat)
kp_info_text = get_kp_info_text(kp_df, 0)
basic_info_header = plat + " — 平台基本信息"
basic_info_text = get_basic_info_text(plat)
sin_fig = plot_feature_trend_with_mc_point(plat, mc_feature, mc_x, mc_y)
com_fig = plot_combined_with_mc_point(plat, mc_feature, mc_x, mc_y)
mc_info_header = "毛刺信息 | 行号: "+str(mc_row_index)
mc_info_text = get_mc_info_text(mc_row_index)

# print(basic_info_header)

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

disabled_style = {
    'background-color': 'gray',
    'color': 'white',
    'cursor': 'not-allowed',
}

button_disabled_style = {**button_style, **disabled_style}

app.layout = html.Div([
    dbc.Container([
        dbc.Row([

            html.Div([
                dcc.Dropdown(
                    FIRST_CLASS,
                    None,
                    id='first-class-dropdown',
                    style={'margin-top': '0px'}
                ),
                dcc.Dropdown(
                    SECOND_CLASS['相关事件'],
                    None,
                    id='second-class-dropdown',
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
                    data=kp_df.to_dict('records'),
                    columns=[{"name": i, "id": i}
                             for i in kp_df.columns],
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
                    page_size=KP_TABLE_PAGE_SIZE,
                    style_table={
                        'height': '400px',
                        'overflowX': 'auto',
                        'margin-top': '10px'
                    },
                    id='kp-table'
                )
            ], style={'width': '17%', 'float': 'right', 'display': 'inline-block',
                      'position': 'absolute',
                      'left': '20px',
                      'margin-top' : '20px'
                      }),

            dbc.Col(
                dbc.Tabs([
                    dbc.Tab([
                        dcc.Dropdown(
                            feature_list_with_abnormal_data,
                            None,
                            id='feature-dropdown',
                            style={'position': 'relative',
                                               'left': '60%', 'width': '50%'}
                        ),
                        dcc.Graph(
                            id='single-series-figure',
                            figure = sin_fig
                        )
                    ],label="存在毛刺的时间序列", style={'position': 'relative', 'left': '0px', 'width': '58%', 'height': '90%'}
                    ),
                    dbc.Tab(dcc.Graph(
                        id='multi-series-figure',
                        figure=com_fig
                    ),
                        label='平台时间序列组合图', style={'position': 'relative', 'left': '0px', 'width': '58%'}
                    ),
                    dbc.Tab(dcc.Graph(
                        id='basic-info-figure',
                        figure=plot_static_data()
                    ),
                        label="平台基本信息图", style={'position': 'relative', 'left': '0px', 'width': '58%'}
                    )
                ], style={'position': 'relative', 'left': '0px', 'width': '58%'}
                ), style={'position': 'relative', 'left': '14%', 'width': '60%','margin-top': '20px'}
            ),

            html.Div([

                dbc.Row(
                    dbc.Col(
                        html.Div([
                            html.H5(basic_info_header,
                                    id='basic-info-header'),
                            dcc.Markdown(
                                f"""
                                {basic_info_text}
                                """, style={'line-height': '0.8', "margin-top": "20px", "margin-bottom": "20px", "overflow": "scroll", }
                            , id = 'basic-info-textbox')
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
                            html.H5(mc_info_header, id='mc-info-header'),
                            dcc.Markdown(
                                f"""
                                        {mc_info_text}
                                        """, id='mc-info-textbox',
                                        style={'line-height': '1.2', "margin-top": "20px", "margin-bottom": "20px", "overflow": "scroll"}
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
                        {kp_info_text}
                        """, id = 'kp-info-textbox', style={'line-height': '1.2', "margin-top": "20px", "margin-bottom": "20px", "overflow": "scroll"}
                    )
                ], style={
                    "width": "230px",
                    "height": "180px",
                    "margin-top" : "0px",
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
                                        placeholder='判断依据',
                                        type='text',
                                        id='reason-input',
                                        style={
                                            'width': '100%', 'margin-top': '0px', 'margin-left': '20px'}
                                    ),
                                    # html.Br(),
                                    dbc.Input(
                                        placeholder='如何修改',
                                        type='text',
                                        id='remarks-input',
                                        style={
                                            'width': '100%', 'margin-top': '10px', 'margin-left': '20px'}
                                    )
                                ], width=9),
                                dbc.Col([
                                    html.Div([
                                        html.Button('OK', id='ok-button', n_clicks=0, style={
                                            **button_disabled_style, 'margin-top': '0px', 'margin-left': '30px'}),
                                        html.Button('Submit', id='submit-button', n_clicks=0, style={
                                            **button_disabled_style, 'margin-top': '10px', 'margin-left': '30px'}, className='btn-submit'),
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
    ), html.Div(id='output1'), html.Div(id='output2'), html.Div(id='output3'), html.Div(id='output4'), # 2 dummy outputs for the callback functions
    
    dcc.ConfirmDialog(
        id='confirm',
        message='Are you sure you want to quit?'
    ),
    
    dcc.ConfirmDialog(
        id='quit-prompt',
        message = "All changes has been saved! \n" +
        "It's safe to close the window! \n" +
        "****** Go back to your terminal and enter Ctrl+C ******"
    )
]
)

# ## Daily Average Figure
# @app.callback(Output('daily-figure', 'figure'),
#               Input('interval-component', 'n_intervals'))
# def update_daily_averages(n):
#     return daily_fig


# --------------------- CallBacks -------------------------


@app.callback(
    Output('output1', 'children'),
    Input('next-button', 'n_clicks')
    )
def update_next(n_clicks):
    global mc_row_index
    
    # print('NEXT TRIGGER')
    
    if mc_row_index >= MAX_MC_ROW_INDEX:
        return dash.no_update
    
    mc_row_index += 1
    
    # print(mc_row_index)
    
    return dash.no_update
    
@app.callback(
    Output('output2', 'children'),
    Input('previous-button', 'n_clicks')
    )
def update_previous(n_clicks):
    global mc_row_index
    
    # print('PREVIOUS TRIGGER')
    
    if mc_row_index <= MIN_MC_ROW_INDEX:  # No previous rows
        return dash.no_update
    
    mc_row_index -= 1
    
    # print(mc_row_index)
    
    return dash.no_update


@app.callback(
    Output('second-class-dropdown', 'options'),
    Input('first-class-dropdown', 'value')
)
def update_sc_dropdown_options(value):
    if value is None:
        return []
    return [{'label': option, 'value': option} for option in SECOND_CLASS[value]]

@app.callback(
    Output('multi-series-figure', 'figure'),
    [Input('previous-button', 'n_clicks'),
    Input('next-button', 'n_clicks')]
)
def update_multi_series_figure(n_clicks1, n_clicks2):
    # print("INDEX", mc_row_index)
    row = mc_df.iloc[mc_row_index]
    plat, mc_feature, mc_x, mc_y = row['平台'], row['时间序列名称'], row['日期'], row['数值']
    com_fig = plot_combined_with_mc_point(plat, mc_feature, mc_x, mc_y)
    return com_fig

@app.callback(
    Output('basic-info-header', 'children'),
    [Input('previous-button', 'n_clicks'),
    Input('next-button', 'n_clicks')]
)
def update_basic_info_header(n_clicks1, n_clicks2):
    # print("INDEX", mc_row_index)
    plat = mc_df.iloc[mc_row_index]['平台']
    return plat + ' - 平台基本信息'

@app.callback(
    Output('basic-info-textbox', 'children'),
    [Input('previous-button', 'n_clicks'),
    Input('next-button', 'n_clicks')]
)
def update_basic_info_text(n_clicks1, n_clicks2):
    # print("INDEX", mc_row_index)
    # global mc_row_index
    plat = mc_df.iloc[mc_row_index]['平台']
    return get_basic_info_text(plat)

@app.callback(
    Output('mc-info-header', 'children'),
    [Input('previous-button', 'n_clicks'),
    Input('next-button', 'n_clicks')]
)
def update_mc_info_header(n_clicks1, n_clicks2):
    # print("INDEX", mc_row_index)
    return "毛刺信息 | 行号: "+str(mc_row_index)

@app.callback(
    Output('mc-info-textbox', 'children'),
    [Input('previous-button', 'n_clicks'),
    Input('next-button', 'n_clicks')]
)
def update_mc_info_text(n_clicks1, n_clicks2):
    # print("INDEX", mc_row_index)
    return get_mc_info_text(mc_row_index)

@app.callback(
    Output('kp-table', 'data'),
    [Input('first-class-dropdown', 'value'),
    Input('second-class-dropdown', 'value'),
    Input('previous-button', 'n_clicks'),
    Input('next-button', 'n_clicks')]
)
def update_datatable(fc, sc, n_clicks1, n_clicks2):
    # global mc_row_index
    global kp_df
    
    # print('Call update_datatable')
    # print([fc, sc, n_clicks1, n_clicks2])
    
    trigger = dash.callback_context.triggered[0]['prop_id']
    if trigger in ['previous-button.n_clicks', 'next-button.n_clicks']:
        row = mc_df.iloc[mc_row_index]
        plat = row['平台']
        # print('Triggered by previous-button or next-button')
        # update data based on "previous" button click
        # if mc_df.iloc[mc_row_index]['平台'] != mc_df.iloc[mc_row_index+1]['平台']:
        # print([plat, sc, fc])
        kp_df = get_platform_df(plat)
        new_data = get_filtered_kp_df(kp_df,fc,sc)
        # print(new_data.head())
        return new_data.to_dict(orient='records')

    elif trigger in ['first-class-dropdown.value', 'second-class-dropdown.value']:
        row = mc_df.iloc[mc_row_index]
        plat = row['平台']
        # print('Triggered by dropdown box')
        # update data based on dropdown box selection
        new_data = get_filtered_kp_df(kp_df,fc,sc)
        # print(new_data.head())
        return new_data.to_dict(orient='records')
    else:
        # print('Triggered by nothing')
        # return the current data if none of the inputs have changed
        return dash.no_update

@app.callback(Output('kp-info-textbox', 'children'),
              [Input('previous-button', 'n_clicks'),
               Input('next-button', 'n_clicks'),
               Input('kp-table', 'active_cell'),
               Input('kp-table', 'page_current')])
def update_kp_info_text(n_clicks1, n_clicks2, active_cell, page_index):
    
    trigger = dash.callback_context.triggered[0]['prop_id']
    if trigger in ['previous-button.n_clicks', 'next-button.n_clicks']:
        return get_kp_info_text(kp_df, 0)
    
    if active_cell:
        row, col = active_cell['row'], active_cell['column_id']
        # print(f'Row index: {row}, Column index: {col}, Page index: {page_index}')
        return get_kp_info_text(kp_df, get_kp_row_index(row, page_index, KP_TABLE_PAGE_SIZE))
    else:
        return get_kp_info_text(kp_df, get_kp_row_index(0, page_index, KP_TABLE_PAGE_SIZE))

@app.callback(
    Output('single-series-figure', 'figure'),
    [Input('feature-dropdown', 'value'),
     Input('previous-button', 'n_clicks'),
     Input('next-button', 'n_clicks')],
    )
def update_single_series_figure(feature, n_clicks1, n_clicks2):
    
    # print("INDEX", mc_row_index)
    
    trigger = dash.callback_context.triggered[0]['prop_id']
    
    row = mc_df.iloc[mc_row_index]
    plat, mc_feature, mc_x, mc_y = row['平台'], row['时间序列名称'], row['日期'], row['数值']
    
    if trigger in ['previous-button.n_clicks', 'next-button.n_clicks']:
        return plot_feature_trend_with_mc_point(plat, mc_feature, mc_x, mc_y)
         
    elif trigger == 'feature-dropdown.value':
        if feature == mc_feature:
            return plot_feature_trend_with_mc_point(plat, mc_feature, mc_x, mc_y)
        elif feature is None:
            return plot_feature_trend_with_mc_point(plat, mc_feature, mc_x, mc_y)
        else:
            return plot_feature_trend(plat, feature)
    else:
        return dash.no_update

@app.callback(
    [Output('ok-button', 'disabled'),
    Output('ok-button', 'style')],
    [Input('radio-items', 'value'),
    Input('reason-input', 'value'),
    Input('remarks-input', 'value'),
    Input('submit-button', 'n_clicks')]
)
def enable_ok_button(value, reason_input, remarks_input, n_clicks):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if trigger == 'submit-button.n_clicks':
        if n_clicks:
            return True, {**button_disabled_style, 'margin-top': '0px', 'margin-left': '30px'}
        else:
            return dash.no_update
    # triggered by value and input
    if value and (reason_input or remarks_input):
        # print("OK button is enabled")
        return False, {**button_style, 'margin-top': '0px', 'margin-left': '30px'}
    # print("OK button is disabled")
    return True, {**button_disabled_style, 'margin-top': '0px', 'margin-left': '30px'}

@app.callback(
    [Output('submit-button', 'disabled'),
    Output('submit-button', 'style')],
    [Input('ok-button', 'n_clicks'),
    Input('submit-button', 'n_clicks')],
    [State('radio-items', 'value'),
    State('reason-input', 'value'),
    State('remarks-input', 'value')]
)
def enable_submit_button(n_clicks1, n_clicks2, value, reason_input, remarks_input):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if trigger == 'submit-button.n_clicks':
        if n_clicks2:
            return True, {**button_disabled_style, 'margin-top': '10px', 'margin-left': '30px'}
        else:
            return dash.no_update
    
    # triggered by ok-button
    if n_clicks1 and value and (reason_input or remarks_input):
        # print("Submit button is enabled")
        return False, {**button_style, 'margin-top': '10px', 'margin-left': '30px'}
    # print("Submit button is disabled")
    return True, {**button_disabled_style, 'margin-top': '10px', 'margin-left': '30px'}

@app.callback(
    Output('output3', 'children'),
    Input('submit-button', 'n_clicks'),
    [State('radio-items', 'value'),
    State('reason-input', 'value'),
    State('remarks-input', 'value')]
    )
def submit_and_write_to_excel(n_clicks, tf, reason, remark):
    
    trigger = dash.callback_context.triggered[0]['prop_id']
    if trigger != 'submit-button.n_clicks':
        # print('triggered by nothing')
        return dash.no_update
    row = list(mc_df.iloc[mc_row_index])
    row[TF_COL_INDEX] = tf
    row[REASON_COL_INDEX] = reason
    row[REVISE_COL_INDEX] = remark
    
    if mc_row_index in checked_mc_info_dict:
        # print('MC info found!')
        checked_mc_row_index = checked_mc_info_dict[mc_row_index][0]
        write_row_to_excel(row, checked_mc_row_index)
    else:
        checked_mc_row_index = write_row_to_excel(row)
        
    print('Writing to excel row #{checked_mc_row_index} : {row}')
    
    checked_mc_info_dict[mc_row_index] = [checked_mc_row_index] + row[1:]
    
    # print(checked_mc_info_dict)
    
    return dash.no_update

@app.callback(
    Output('confirm', 'displayed'),
    [Input('save-quit-button', 'n_clicks'),
    Input('confirm', 'submit_n_clicks')]
)
def display_confirm(n_clicks1, n_clicks2):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if trigger == 'save-quit-button.n_clicks':
        if n_clicks1 is not None:
            return True
        return False
    elif trigger == 'confirm.submit_n_clicks':
        if n_clicks2 is not None:
            return False
        return True
    
    return False

@app.callback(
    Output('quit-prompt', 'displayed'),
    Input('confirm', 'submit_n_clicks'),
    # State('confirm', 'displayed')
)
def save_and_quit(n_clicks):
    # print("Save and quit is called")
    # print([n_clicks])
    if n_clicks is not None:
        print("------- Succesfully save and exit -------")
        print("------- Enter Ctrl+C to quit the server -------")
        write_curr_line_no(mc_row_index)
        # print("System existing")
        # server.shutdown()
        return True
        
    return False

if __name__ == '__main__':
    app.run_server(debug=True)