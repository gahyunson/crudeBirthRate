import pandas as pd
import numpy as np
import re
fertility = pd.read_csv('project_data/합계출산.csv', encoding='utf-8')
fertility.columns = ['합계출산;'+i for i in fertility.columns]
hdi = pd.read_csv('project_data/인간개발지수.csv',encoding='utf-8', header=[0,1])
hdi.columns = [';'.join(i) for i in hdi.columns]
hdi['국가별;국가별'] = hdi['국가별;국가별'].apply(lambda x: x.strip())
hdi = hdi.replace(',','')
hdi.iloc[:,-1] = hdi.iloc[:,-1].str.replace(',','') # comma문제 해결
gdp = pd.read_csv('project_data/국민소득.csv', encoding='utf-8', header=[0,1])
gdp.columns = [';'.join(i) for i in gdp.columns]
urban = pd.read_csv('project_data/도시화율.csv', encoding='utf-8')
urban.columns = ['도시화율;'+i for i in urban.columns]
pop = pd.read_csv('project_data/인구_동향.csv', encoding='utf-8', header=[0,1])
pop.columns = [';'.join(i) for i in pop.columns]
action_man = pd.read_excel('project_data/경제활동참여율(남).xlsx').drop(columns='대륙')
action_woman = pd.read_excel('project_data/경제활동참여율(여).xlsx').drop(columns='대륙')
action_man = action_man.rename(columns = {'국가':'국가별;국가별',
                                          '경제활동참여율;2020':'경제활동참여율;남자'})
action_woman = action_woman.rename(columns = {'국가':'국가별;국가별',
                                              '경제활동참여율;2020':'경제활동참여율;여자'})
edu = pd.read_excel('project_data/교육정도별_취학률.xlsx', header=[0,1])
edu[('국가별','국가별')] = np.repeat(edu[('국가별','국가별')]\
                               [edu[('국가별','국가별')].isna()==False].values,
                               3)
edu[('국가별','국가별')] = edu[('국가별','국가별')].apply(lambda x: x.strip())
edu.columns = [';'.join(i) for i in edu.columns]
edu = pd.concat([edu.pivot(values = i, columns = '성별;성별', index = '국가별;국가별')
                for i in edu.columns[2:]], keys = [i for i in edu.columns[2:]],
                axis=1)
edu = edu.replace('-',np.nan)
def all_na(df_col):
    not_na = df_col[df_col.isna()==False]
    if len(not_na)>0:
        return not_na.iloc[0]
    else:
        return np.nan
for i in range(4):
    first_name = edu.columns[9*i][0].split(';')[0]
    for j in range(3):
        last_name = edu.columns[9*i+j][1]
        edu[(first_name,last_name)] = edu.iloc[:,9*i+j:9*(i+1)+j:3].apply(all_na,
                                                                          axis=1)
edu = edu.iloc[:,-12:]
edu.columns = [';'.join(i) for i in edu.columns]
edu[edu.index.name] = edu.index
edu.index = range(len(edu))
merged_df = gdp.copy()
merged_df
for file in (fertility, urban, hdi, pop, edu, action_man, action_woman):
    try:
        merged_df = merged_df.merge(file,
                              'outer',
                              left_on = '국가;국가',
                              right_on = '국가별;국가별',
                              )
    except:
        merged_df = merged_df.merge(file,
                              'outer',
                              left_on = '국가;국가',
                              right_on = file.columns[file.columns.str.endswith('국가별')][0],
                              )
nation_column = merged_df[merged_df.columns[merged_df.columns.str.contains('국가(별|;)')]]
merged_df = merged_df.drop(
    columns = merged_df.columns[merged_df.columns.str.contains('국가(별|;)')])
merged_df['국가'] = nation_column.apply(lambda x: x[x.isna()==False].iloc[0], axis=1)
duplicate = merged_df['국가'].value_counts()[merged_df['국가'].value_counts()>1].index
rm_na_df = merged_df[merged_df['국가'].isin(duplicate)].\
                                groupby('국가').apply(lambda x: x.apply(all_na))
merged_df = merged_df.drop(index = merged_df[merged_df['국가'].isin(duplicate)].index)
final_data = pd.concat([merged_df,rm_na_df], axis=0)
final_data.set_index(['국가'], inplace=True)
final_data.replace('-',np.NaN, inplace = True)
#final_data.to_csv('210809자료합친파일.csv', encoding="utf-8-sig")
for col in final_data.columns:
    final_data[col] = final_data[col].apply(lambda data : data if pd.isna(data) else re.findall('[0-9.]+',str(data))[0])
final_data = final_data.astype(float)
final_data.to_csv('210809자료합친파일.csv', encoding="utf-8-sig")
