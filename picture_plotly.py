import plotly.express as px
import pandas as pd
import platform

final_data=pd.read_csv('210809자료합친파일.csv', index_col = 0)
final_data['국가명'] = final_data.index
def makeDataframe(col, data):
    data_df=data[[col,'합계출산;2020','국가명']]
    data_df=data_df[data_df['국가명']!='세계']
    data_df.sort_values(col, ascending=False, inplace=True)
    data_df=data_df.dropna()
    return data_df

def plotlyGraph(df,col):
    fig = px.scatter(df,
                     x = '합계출산;2020',
                     y = col,
                     hover_data = ['국가명'],
                     title = col+'& Birth rate',
                     labels = {'합계출산;2020':'2020 birthrate'})
    fig.write_html('figure/'+str(col)+'.html')

gdp_birth_gh=makeDataframe('2019;국내총생산(GDP $)',final_data)
city_birth_gh=makeDataframe('도시화율;2020',final_data)
edu_birth_gh=makeDataframe('평균교육기간(년);2018',final_data)
gni_birth_gh=makeDataframe('1인당 GNI(구매력환산기준 2011) (달러);2018',final_data)
improve_birth_gh=makeDataframe('2020;연간 인구증가율',final_data)
consumer_birth_gh = makeDataframe('소비자물가지수;2019',final_data)
for feature in ('gdp','city','edu','gni','improve','consumer'):
    df = eval(feature+'_birth_gh')
    plotlyGraph(df, df.columns[0])
