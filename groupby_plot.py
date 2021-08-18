import pandas as pd
import numpy as np
from matplotlib import rcParams
import matplotlib.pyplot as plt

data = pd.read_csv('210809자료합친파일.csv', index_col = 0)
def na_filler(column):
    col_in_question = data.loc[:,data.columns.str.contains(column, regex=False)]
    data.drop(columns = data.columns[data.columns.str.contains(column, regex=False)],
              inplace=True)
    data[column] = col_in_question.apply(na_fill, axis = 1)
def na_fill(df):
    i=-1
    datum = df.iloc[i]
    while pd.isna(datum):
        i-=1
        try:
            datum = df.iloc[i]
        except:
            return np.nan
    return datum
na_filler('GDP')
na_filler('합계출산')
grouped_data = data.groupby('sub-region').mean()
explain = grouped_data.drop(columns = '합계출산')
explain.drop(columns = explain.columns[explain.columns.str.startswith('학년전교육')],
             inplace = True)
explain.columns = ['도시화율','교육기간','GNI','인구증가율','유소년인구','생산가능인구','노년인구','초등남자','초등여자','초등합계','중등남자','중등여자','중등합계','고등남자','고등여자','고등합계','경제참여율남자','경제참여율여자','물가지수','GDP']
features = np.array(explain.columns).reshape((4,5))

explain['colors'] = ['blue','orange','orange','green','red','blue','blue',
                     'black','red','green','blue','orange','orange','green',
                     'black','orange','green']
explain['markers'] = ['>','>','o','>','>','<','v',
                      '>','<','<','^','v','^','v',
                      '<','<','^']
explain['합계출산'] = grouped_data['합계출산']
rcParams['font.family']=['Malgun Gothic']
rcParams['axes.unicode_minus']=False
fig, axes = plt.subplots(4, 5, sharex = True) # constrained_layout=True without legend
fig.suptitle('세계 지역별 합계출산률과 여러 변수들의 관계')
plt.subplots_adjust(wspace=.4)
for i in range(4):
    for j in range(5):
        for k in range(len(explain.index)):
            df = explain[[features[i,j],'합계출산','colors','markers']]
            axes[i,j].plot(df.iloc[k,1], df.iloc[k,0],
                           c = df.iloc[k,2], marker = df.iloc[k,3],
                           label = df.index[k], linestyle = 'None')
        axes[i,j].set_ylabel(features[i,j])
axes[-1,0].legend(loc = 'upper left', ncol = 6,
                  bbox_to_anchor = (-.1, -.1), frameon = False)
plt.show()
