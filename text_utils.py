import pandas as pd
import numpy as np
import csv
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils import *

kp_df = pd.read_excel('data/平台画像数据库.xlsx',sheet_name='知识词典').dropna(subset=['相关平台'])

cleaned_basic_info = pd.read_csv("data/平台基本信息(452个+已清洗).csv")
cleaned_basic_info = cleaned_basic_info.set_index('FullName')

mc_df = pd.read_excel("data/毛刺机器校对(全部9162).xlsx")
cleaned_mc_info = mc_df.drop(columns=['是否确实为毛刺？','编号','平台','如何修改','证据/依据','备注'])

def get_platform_df(platform):
    plat_df = kp_df[kp_df['相关平台'].str.contains(platform)].get(['一级类','二级类','知识词典'])
    return plat_df

def parseDic(str):
    return {pair.split(': ')[0]: pair.split(': ')[1] for pair in str[1:-1].replace("'", "").split(', ')}

def get_basic_info_text(platform):
    basic_info_dict = dict(cleaned_basic_info.loc[platform])
    info_list = [f"**{k}:** {v}" for k, v in basic_info_dict.items()]
    info_text = "\n\n".join(info_list)
    return "\n\n" + info_text.strip()

def get_mc_info_text(row_index):
    mc_info_dict = dict(cleaned_mc_info.iloc[row_index])
    info_list = [f"**{k}:** {v}" for k, v in mc_info_dict.items()]
    info_text = "\n\n".join(info_list)
    return "\n\n" + info_text.strip()

def get_kp_info_text(plat_df, row_index):
    kp_dict = parseDic(plat_df['知识词典'].iloc[row_index])
    info_list = [f"**{k}:** {v}" for k, v in kp_dict.items()]
    info_text = "\n\n".join(info_list)
    return "\n\n" + info_text.strip()