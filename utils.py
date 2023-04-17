import pandas as pd
import numpy as np
import csv
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_dataset():
    # 导入需要的数据
    t1 = np.load(r'data/data_3darray.npy')
    calendar = pd.read_csv(r'data/standard_calendar.csv')
    platforms = pd.read_csv(r'data/standard_platform.csv')
    features = pd.read_csv(r'data/feature.csv')
    static_data = pd.read_csv('data/1031个平台基本信息.csv')
    mc = pd.read_excel(r'data/疑似毛刺数据列表.xlsx')
    mc = mc.set_index("时间序列名称")
    t1 = t1.astype(np.float32)

    # 分别设置1、2、3维的标签
    index1 = pd.Series(["TradingVolume","AveReturn","InvestorNum","AveLimTime","LoanNum","CumulateRepay","F30Repay","F60Repay","RegistedCapital","PlatformBackground","Unknown1","Unknown2"])
    index2 = pd.Series(platforms.values.flatten())
    index3 = pd.Series(calendar.values.flatten())

    # 展开三维数组
    value = t1.flatten()
    value = pd.Series(value)
    value.name = 'value'

    # 展开标签
    import itertools

    # index的笛卡尔乘积。注意高维在前，低维在后。
    prod = itertools.product(index3,index2,index1)

    # 转换成DataFrame
    prod = pd.DataFrame([x for x in prod])
    prod.columns = ["日期","平台","特征"]

    # 合并成一个DataFrame
    df = pd.concat([prod,value],axis=1)
    df["日期"] = pd.to_datetime(df["日期"])

    df = df.set_index(['平台','日期','特征'])
    df = df.unstack("特征")   # 解开“特征”列
    df.columns = ["AveLimTime","AveReturn","CumulateRepay","F30Repay","F60Repay","InvestorNum","LoanNum","PlatformBackground","RegistedCapital","TradingVolume","Indicator1","Indicator2"]
    df.columns.names = ["特征"]


    # # 数据清洗
    df = df.dropna(how="all")  # 去掉缺失值
    
    return df, static_data, platforms, features


