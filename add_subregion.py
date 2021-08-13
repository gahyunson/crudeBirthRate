import pandas as pd
# 출처: https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv
subregion = pd.read_csv('지역구분.csv')
iso_code = pd.read_csv('외교부_국가·지역별 표준코드_20201231.csv', encoding='cp949')
final_data = pd.read_csv('210809자료합친파일.csv')
exception = {'타이완':'대만',
        '대한민국':'한국',
        '호주':'오스트레일리아',
        '콩고공화국':'콩고',
        '콩고민주공화국(DR콩고)':'콩고민주공화국',
        '키르기즈':'키르기스스탄',
        '모리타니아':'모리타니'}
for key, value in exception.items():
    iso_code['국가명(국문)'] = iso_code['국가명(국문)'].replace(key, value)
iso_subregion = iso_code.merge(subregion, 'left',
        left_on = 'ISO(2자리)', right_on = 'alpha-2')[
                ['국가명(국문)','ISO(2자리)','sub-region']
                ]
iso_subregion.columns = ['국가']+list(iso_subregion.columns[1:])
final_data = final_data.merge(iso_subregion, 'left', on = '국가')
final_data.to_csv('210809자료합친파일.csv', index=False)
