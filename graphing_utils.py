import pandas as pd
import numpy as np
import csv
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_processing_utils import *

df, static_data, platforms, features = load_dataset()

platform_list = list(platforms.values.flatten())
feature_list = list(features['Feature'])
feature_list_with_abnormal_data = ['TradingVolume','AveReturn','InvestorNum','AveLimTime',
                                   'LoanNum','CumulateRepay','F30Repay','F60Repay']
units = ["万","%","人","月","人","万","万","万"]
feature_unit_dic = {feature_list_with_abnormal_data[i] : units[i] for i in range(8)}


# 画图参数
template= 'plotly_white'
title_color = '#000000'
color1 = "#707377"  #"#FF0505"
color2 = "#0F3680"     #"#0F3680"
color3 = "#f32247"
abnormal_color = "#00FFFF"
opacity = 0.5
subplot_height = 260
subplot_width = 240
subplot_font_size = 8
subplot_mark_size = 8
subplot_line_width = 0.8
rows = 2
cols = 4
height = rows * subplot_height
width = cols * subplot_width
font_size = 15
mark_size = 15
line_width = 1.6

def get_all_data(platform,feature,line_width = line_width):  # 0
    data_series = df.loc[platform][feature]
    time = np.array(data_series.index)
    
    data_1 = go.Scatter(
        x=time,
        y=np.array(data_series.values),
        legendgroup='Data',  # Groups traces belonging to the same group in the legend 
        name='feature',
        line=dict(color = color2,
                    width=line_width)
    )
    return data_1

def get_abnormal_data(platform,feature,line_width = line_width, mark_size = mark_size):
    Abnormal_values = df.loc[platform][feature].where(
    (df.loc[platform][feature]>(df.loc[platform][feature].mean()+4*df.loc[platform][feature].std()))|
                                (df.loc[platform][feature]<(df.loc[platform][feature].mean()-4*df.loc[platform][feature].std()))
                               )
    time = np.array(df.loc[platform][feature].index)
    data_2 = go.Scatter(
        x=time,
        y=pd.Series(Abnormal_values.values),
        name='Abnormal data',
        line=dict(color = color3,
                    width=line_width
                ),
        mode = 'markers+lines+text',
        text = "O",
        textposition='bottom right',
        textfont={'color': color3, 'size':mark_size}
        )
            
    return data_2

def get_particular_mc_data(mc_x, mc_y):
    data_3 = go.Scatter(
        x=[mc_x],
        y=[mc_y],
        name='Particular abnormal data point',
        line=dict(color = abnormal_color,
                    width=line_width
                ),
        mode = 'markers',
        # text = "{:.2f}".format(mc_y),
        # textposition='top right',
        # textfont={'color': abnormal_color, 'size' : mark_size},
        marker={'size':mark_size+5, 'symbol' : "star"}
        )
            
    return data_3


def plot_combined(platform):
    grid = [[{} for _ in range(cols)] for i in range(rows)]
    fig = make_subplots(rows=rows, cols=cols, specs=grid,
        subplot_titles=(tuple(feature_list_with_abnormal_data)))

    for i,feature in enumerate(feature_list_with_abnormal_data):

        data_1 = get_all_data(platform,feature,line_width=subplot_line_width)
        data_2 = get_abnormal_data(platform,feature,mark_size = subplot_mark_size,line_width = subplot_line_width)

        row = i // cols + 1
        col = i % cols + 1

        fig.add_trace(data_1, row = row, col = col)

        fig.add_trace(data_2, row = row, col = col)
        
        # 更改y轴单位
        fig.update_yaxes(ticksuffix = units[i],row=row,col=col)
        

    #  -------------- 更新图片外观 ------------------

    # 更新大小和底色
    fig.update_layout(
    width=width,
    height=height,
    template=template,
    font = dict(
        size = subplot_font_size, # 整张图所有文字注释的字体
        color = '#000000'
    )
    )

    # 调节每个subplot的标题的字体大小 
    #         fig.update_annotations(font_size=45) 

    # 选择不显示legend
    fig.update(layout_showlegend=False)

    # 优化X轴的注释(显示日期的格式)
    fig.update_xaxes(
        ticks= "outside",
                ticklabelmode= "period", 
                tickcolor= "black", 
                ticklen=15,
                #title_font_size=18,
                minor=dict(
                    ticklen=7,
                    #tickwidth=5,
                    #dtick=30*24*60*60*1000,  
                    #tick0="2016-07-03", 
                    griddash='dot', 
                    gridcolor='white'),
            tickangle=20      # 更改日期的倾斜度, 20度的效果不错
            )
    

    fig.update_layout(
                        height=height,
                        width=width,
                        title={
                            'text': platform,
                            'x': 0.5,
                            'y':0.95,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font': {'size':25}
                            }
            )
        
    return fig

def plot_feature_trend_with_mc_point(platform, feature, mc_x, mc_y):
    fig = go.Figure()
    data_1 = get_all_data(platform,feature,line_width=line_width)
    data_2 = get_abnormal_data(platform,feature,mark_size=mark_size,line_width=line_width)
    data_3 = get_particular_mc_data(mc_x, mc_y)
    
    fig.add_trace(data_1)

    fig.add_trace(data_2)
    
    fig.add_trace(data_3)
    
    fig.update_yaxes(ticksuffix = feature_unit_dic[feature])
    
    # 更新大小和底色
    fig.update_layout(
    width=width,
    height=height,
    template=template,
    font = dict(
        size = font_size, # 整张图所有文字注释的字体
        color = '#000000'
    )
    )

    # 调节每个subplot的标题的字体大小 
    #         fig.update_annotations(font_size=45) 

    # 选择不显示legend
    fig.update(layout_showlegend=False)

    # 优化X轴的注释(显示日期的格式)
    fig.update_xaxes(
        ticks= "outside",
                ticklabelmode= "period", 
                tickcolor= "black", 
                ticklen=15,
    #                     title_font_size=18,
                minor=dict(
                    ticklen=7,
    #                      tickwidth=5,
                    #dtick=30*24*60*60*1000,  
                    #tick0="2016-07-03", 
                    griddash='dot', 
                    gridcolor='white'),
            tickangle=20      # 更改日期的倾斜度, 20度的效果不错
            )


    fig.update_layout(
                        height=height-38,
                        width=width,
                        xaxis=dict(rangeslider=dict(visible = True), type = "date", showgrid = False),
                        title={
                            'text': feature,
                            'x': 0.5,
                            'y':0.92,
                            'xanchor': 'center',
                            'yanchor': 'top'}
            )
    
    return fig

def plot_combined_with_mc_point(platform, mc_feature, mc_x, mc_y):
    grid = [[{} for _ in range(cols)] for i in range(rows)]
    fig = make_subplots(rows=rows, cols=cols, specs=grid,
        subplot_titles=(tuple(feature_list_with_abnormal_data)))

    for i,feature in enumerate(feature_list_with_abnormal_data):

        data_1 = get_all_data(platform,feature,line_width=subplot_line_width)
        data_2 = get_abnormal_data(platform,feature,mark_size = subplot_mark_size,line_width = subplot_line_width)

        row = i // cols + 1
        col = i % cols + 1

        fig.add_trace(data_1, row = row, col = col)

        fig.add_trace(data_2, row = row, col = col)
        
        if feature == mc_feature:
            data_3 = get_particular_mc_data(mc_x, mc_y)
            fig.add_trace(data_3, row = row, col = col)
        
        # 更改y轴单位
        fig.update_yaxes(ticksuffix = units[i],row=row,col=col)
        

    #  -------------- 更新图片外观 ------------------

    # 更新大小和底色
    fig.update_layout(
    width=width,
    height=height,
    template=template,
    font = dict(
        size = subplot_font_size, # 整张图所有文字注释的字体
        color = '#000000'
    )
    )

    # 调节每个subplot的标题的字体大小 
    #         fig.update_annotations(font_size=45) 

    # 选择不显示legend
    fig.update(layout_showlegend=False)

    # 优化X轴的注释(显示日期的格式)
    fig.update_xaxes(
        ticks= "outside",
                ticklabelmode= "period", 
                tickcolor= "black", 
                ticklen=15,
                #title_font_size=18,
                minor=dict(
                    ticklen=7,
                    #tickwidth=5,
                    #dtick=30*24*60*60*1000,  
                    #tick0="2016-07-03", 
                    griddash='dot', 
                    gridcolor='white'),
            tickangle=20      # 更改日期的倾斜度, 20度的效果不错
            )
    

    fig.update_layout(
                        height=height,
                        width=width,
                        title={
                            'text': platform,
                            'x': 0.5,
                            'y':0.95,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font': {'size':25}
                            }
            )
        
    return fig

def plot_feature_trend(platform, feature):
    fig = go.Figure()
    data_1 = get_all_data(platform,feature,line_width=line_width)
    data_2 = get_abnormal_data(platform,feature,mark_size=mark_size,line_width=line_width)
    
    fig.add_trace(data_1)

    fig.add_trace(data_2)
    
    
    fig.update_yaxes(ticksuffix = feature_unit_dic[feature])
    
    # 更新大小和底色
    fig.update_layout(
    width=width,
    height=height,
    template=template,
    font = dict(
        size = font_size, # 整张图所有文字注释的字体
        color = '#000000'
    )
    )

    # 调节每个subplot的标题的字体大小 
    #         fig.update_annotations(font_size=45) 

    # 选择不显示legend
    fig.update(layout_showlegend=False)

    # 优化X轴的注释(显示日期的格式)
    fig.update_xaxes(
        ticks= "outside",
                ticklabelmode= "period", 
                tickcolor= "black", 
                ticklen=15,
    #                     title_font_size=18,
                minor=dict(
                    ticklen=7,
    #                      tickwidth=5,
                    #dtick=30*24*60*60*1000,  
                    #tick0="2016-07-03", 
                    griddash='dot', 
                    gridcolor='white'),
            tickangle=20      # 更改日期的倾斜度, 20度的效果不错
            )


    fig.update_layout(
                        height=height-38,
                        width=width,
                        xaxis=dict(rangeslider=dict(visible = True), type = "date", showgrid = False),
                        title={
                            'text': feature,
                            'x': 0.5,
                            'y':0.92,
                            'xanchor': 'center',
                            'yanchor': 'top'}
            )
    
    return fig

def plot_static_data():
    fig = make_subplots(
        rows=4, cols=2,
        specs=[[{}, {"rowspan": 2,"type": "domain"}],
            [{}, None],
            [{"rowspan": 2, "colspan": 2}, None],
            [None, None]
            ],
            
        #print_grid=True,
        subplot_titles=['注册资本', '平台背景', '', '平台上线时间'])


    fig.add_trace(go.Box(x=static_data.get('RegistedCapital')*10000,name="", legendgroup=None), row=1, col=1)
    fig.update_xaxes(title_text="(标准刻度)", row=1, col=1)
    fig.add_trace(go.Box(x=static_data.get('RegistedCapital')*10000, name=""), row=2, col=1)
    fig.update_xaxes(title_text="(对数刻度)", type="log", row=2, col=1)
    fig.add_trace(go.Pie(labels=static_data[~static_data.get('PlatformBackground').isnull()].get('PlatformBackground'), pull=[0] + [0.2 for _ in range(1000)], name='Pie'), row=1, col=2)
    fig.add_trace(go.Histogram(x = static_data.get('RegistedDate'), name = 'Hist', xbins = dict(size='M1')), row=3, col=1)

    fig.update_xaxes(
            #linecolor = '#000000',
            ticks= "outside",
            linewidth = 1.5,
            dtick='M6',
            tickangle=20,
            row = 3,
            col = 1)

    for trace in fig['data']:
        if(trace['name'] != 'Pie'):
            trace['showlegend'] = False

    fig.update_layout(
        height=height, 
        width=width,
        bargap = 0.2, 
        #title_text="specs examples",
        template=template,
        # legend=dict(x=0.96,y=1),
        title = dict(
            text = '<b>{0}<b>'.format('网贷平台基本信息图'),
            x = 0.10,
            y = 0.96,
            font = dict(
                size = 30,
                color = title_color
            ))
    )
    
    return fig