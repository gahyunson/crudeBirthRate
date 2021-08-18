import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import platform
import folium
import json

final_data=pd.read_csv('210809자료합친파일.csv', index_col = 0)
final_data['국가명'] = final_data.index
def makeDataframe(col, data):
    data_df=data[[col,'합계출산;2020','국가명']]
    data_df=data_df[data_df['국가명']!='세계']
    data_df.sort_values(col, ascending=False, inplace=True)
    data_df=data_df.dropna()
    return data_df

def saveGraph(df,col,log=False):
    if platform.system()=="Darwin":
        rcParams['font.family']=['AppleGothic']
    elif platform.system()=="Windows":
        rcParams['font.family']=['Malgun Gothic']
    rcParams['axes.unicode_minus']=False
    
    plt.rcParams['figure.figsize']=[15,10]
    
    plt.plot('합계출산;2020',
             col,
             data = df, 
             linestyle='none', 
             marker='o', 
             markersize=10,
             color='blue', 
             alpha=0.5)

    plt.title(col+'& Birth rate', fontsize=20)
    plt.xlabel('2020 birthrate', fontsize=14)
    plt.ylabel(col, fontsize=14)
    if log:
        plt.yscale('log')
    plt.hlines(df[col].mean(),
               df['합계출산;2020'].min(),
               df['합계출산;2020'].max(),
             color='gray',
             linestyle='--',
             linewidth = 2)
    plt.vlines(df['합계출산;2020'].mean(),
               df[col].min(),
               df[col].max(),
             color='gray',
             linestyle='--',
             linewidth = 2)
    
    plt.savefig('figure/'+str(col)+'.png') # 그림 저장하기
    plt.clf() # 새 도화지 준비하기

gdp_birth_gh=makeDataframe('2019;국내총생산(GDP $)',final_data)
city_birth_gh=makeDataframe('도시화율;2020',final_data)
edu_birth_gh=makeDataframe('평균교육기간(년);2018',final_data)
gni_birth_gh=makeDataframe('1인당 GNI(구매력환산기준 2011) (달러);2018',final_data)
improve_birth_gh=makeDataframe('2020;연간 인구증가율',final_data)
consumer_birth_gh = makeDataframe('소비자물가지수;2019',final_data)
for feature in ('gdp','city','edu','gni','improve','consumer'):
    df = eval(feature+'_birth_gh')
    if feature == 'gdp':
        saveGraph(df, df.columns[0], log = True)
    else:
        saveGraph(df, df.columns[0])


######## 지도저장하기
with open ('countries_data.json', 'r', encoding='cp949') as file:
    countries_data = json.load(file)

maintain_birthrate_world_map = folium.Map(location = [38, 38], tiles='CartoDB positron',
    zoom_start=2)

below_maintain_birthrate = final_data[final_data['합계출산;2020'] > 2.1]

folium.Choropleth(geo_data = countries_data,
        data = below_maintain_birthrate,
        columns = ['국가명','합계출산;2020'],
        key_on = 'properties.korname',
        fill_color = 'GnBu',
        nan_fill_color = None,
        fill_opacity = 0.5,
        line_color = 'white',
        legend_name = '2020합계출산률(2.1 이하 국가)',
        ).add_to(maintain_birthrate_world_map)

maintain_birthrate_world_map.save('figure/2020합계출산률(2.1 이하 국가).html')

pop_incrate_world_map = folium.Map(location = [38, 38], tiles='CartoDB positron',
    zoom_start=2)

folium.Choropleth(geo_data = countries_data,
        data = final_data[final_data['2020;연간 인구증가율'] > 0],
        columns = ['국가명','2020;연간 인구증가율'],
        key_on = 'properties.korname',
        fill_color = 'YlGn',
        nan_fill_color = 'white',
        fill_opacity = 0.5,
        line_color = 'white',
        legend_name = '2020 국가별 인구 증가율',
        ).add_to(pop_incrate_world_map)

pop_incrate_world_map.save('figure/인구가 증가한 국가.html')

pop_decrate_world_map = folium.Map(location = [38, 38], tiles='CartoDB positron',
    zoom_start=2)

folium.Choropleth(geo_data = countries_data,
        data = final_data[final_data['2020;연간 인구증가율'] < 0],
        columns = ['국가명','2020;연간 인구증가율'],
        key_on = 'properties.korname',
        fill_color = 'OrRd',
        nan_fill_color = 'white',
        fill_opacity = 0.5,
        line_color = 'white',
        legend_name = '2020 국가별 인구 증가율',
        ).add_to(pop_decrate_world_map)

pop_decrate_world_map.save('figure/인구가 감소한 나라.html')

differ_pop_world_map = folium.Map(location = [38, 38], tiles='CartoDB positron',
    zoom_start=2)

folium.Choropleth(geo_data = countries_data,
        data = final_data[(final_data['2020;연간 인구증가율'] > 0) &(final_data['합계출산;2020'] < 2.1)],
        columns = ['국가명','2020;연간 인구증가율'],
        key_on = 'properties.korname',
        fill_color = 'GnBu',
        nan_fill_color = 'white',
        fill_opacity = 0.5,
        line_color = 'white',
        legend_name = '2020 국가별 인구 증가율',
        ).add_to(differ_pop_world_map)

differ_pop_world_map.save('figure/출산율이 2.1미만임에도 인구가 증가한 나라.html')
