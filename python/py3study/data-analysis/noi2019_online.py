import numpy as np
import pandas as pd


url = 'http://www.noi.cn/RequireFile.do?fid=5B9HgmmE&attach=n'
dfs = pd.read_html(url, header=0, flavor=['bs4'])
df = dfs[0]
print(df)
print(df.groupby('省份').sum().sort_values(by='总分（不含笔试100分）', ascending=False)[:20])
print(df.groupby('所在学校').sum().sort_values(by='总分（不含笔试100分）', ascending=False)[:20])
print(df.groupby('年级（暑假前）').sum().sort_values(by='总分（不含笔试100分）', ascending=False)[:20])

print(df.groupby('省份').count().sort_values(by='总分（不含笔试100分）', ascending=False))
print(df.groupby('所在学校').count().sort_values(by='总分（不含笔试100分）', ascending=False))
print(df.groupby('年级（暑假前）').count().sort_values(by='总分（不含笔试100分）', ascending=False))