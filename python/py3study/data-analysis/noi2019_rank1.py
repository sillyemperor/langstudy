import numpy as np
import pandas as pd


url = 'http://www.noi.cn/RequireFile.do?fid=mq6t95Q7&attach=n'
dfs = pd.read_html(url, header=0, flavor=['bs4'], skiprows=[0,1,54,55,158,159])
df = dfs[0]
print(df.columns)
# print(df[150:200])
# print(df[153:155])
print(df.loc[:, ['省份', '总分']].groupby('省份').sum().sort_values(by='总分', ascending=False))
print(df.loc[:, ['年级', '总分']].groupby('年级').sum().sort_values(by='总分', ascending=False))
print(df.loc[:, ['学校(全称)', '总分']].groupby('学校(全称)').sum().sort_values(by='总分', ascending=False)[:20])

print(df.loc[:, ['省份', '总分']].groupby('省份').count().sort_values(by='总分', ascending=False))
print(df.loc[:, ['年级', '总分']].groupby('年级').count().sort_values(by='总分', ascending=False))
print(df.loc[:, ['学校(全称)', '总分']].groupby('学校(全称)').count().sort_values(by='总分', ascending=False)[:20])
