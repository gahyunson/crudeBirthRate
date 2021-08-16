import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
country_data = pd.read_csv('210809자료합친파일.csv', index_col = 0)
country_data_with_answer = country_data[pd.isna(country_data['합계출산;2015'])==False]
country_data_in_question = country_data[pd.isna(country_data['합계출산;2015'])]
explanatory_variables = ['1인당 GNI(구매력환산기준 2011) (달러);2018',
                  '평균교육기간(년);2018', '경제활동참여율;여자',
                  '도시화율;2020','sub-region']
X = country_data_with_answer[explanatory_variables]
y = country_data_with_answer['합계출산;2015']

preprocess_cat = Pipeline(steps = [ # 어느 곳에 속한 지 모르면 missing으로 지역이름 설정
    ('imputer', SimpleImputer(strategy = 'constant', fill_value = 'missing')),
    ('encoder', OneHotEncoder( # 각 지역을 하나의 설명변수로 설정(encode)
        handle_unknown = 'ignore')), # when encountering unknown, encode all zero
    ])
preprocess_num = Pipeline(steps = [
    ('imputer', SimpleImputer(strategy = 'median')), # NaN를 중앙값으로 변경
    ])
preprocess = ColumnTransformer(
    transformers = [
        ('numerizer', preprocess_num, explanatory_variables[:-1]),
        ('categorizer', preprocess_cat, explanatory_variables[-1:]),
        ])

reg = Pipeline(steps = [('preprocessor', preprocess),
                        ('regressor', LinearRegression()),
                        ])
reg.fit(X, y) # 선형 회귀분석
print('RMSE: '+str(mean_squared_error(y, reg.predict(X)))) # 평균오차 산정
print(
    pd.Series(
        reg.predict(country_data_in_question[explanatory_variables]),
        index = country_data_in_question.index,
        name = '출산율이 NaN인 국가의 출산율 예측치')
    )
print(
    pd.Series(
        reg.named_steps['regressor'].coef_,
        index = explanatory_variables[:-1] + \
        list(reg.named_steps['preprocessor'].named_transformers_['categorizer'].\
             named_steps['encoder'].categories_[0]),
        name = '각 설명변수의 회귀계수')
    )
