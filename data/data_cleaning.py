import pandas as pd
import json

## import csvs
df1 = pd.read_csv("county_ages.csv")
df2 = pd.read_csv("county_demographics.csv")
df3 = pd.read_csv("countypres_2000-2016.csv")
df4 = pd.read_json("precincts-with-results.geojson.gz")
df4['features'][0]


# load data using Python JSON module
with open('precincts-with-results.geojson.gz','r', encoding="utf8") as f:
    data = json.loads(f.read())

df = pd.read_csv('precincts-with-results.geojson.gz', compression='gzip', header=0, sep=' ', quotechar='"', error_bad_lines=False)


# Flatten data
df_nested_list = pd.json_normalize(data, record_path =['features'])




## change age columns to match what I want
df1 = df1.drop(['Unnamed: 0'], axis = 1)
df2 = df2.drop(['Unnamed: 0'], axis = 1)

## MALE
## less than 30
m_le_30 = ['M5','M5-9', 'M10-14', 'M15-17', 'M18-19', 'M20', 'M21', 'M22-24', 'M25-29']
df1['male_le_30'] = df1[m_le_30].sum(axis = 1)
df1 = df1.drop(df1[m_le_30], axis = 1)

## 30 - 45
m_ge_30_le_45 = ['M30-34', 'M35-39', 'M40-44']
df1['male_ge_30_le_45'] = df1[m_ge_30_le_45].sum(axis = 1)
df1 = df1.drop(df1[m_ge_30_le_45], axis = 1)

## 45 - 65
m_ge_45_le_65 = ['M45-49', 'M50-54', 'M55-59', 'M60-61', 'M62-64']
df1['male_ge_45_le_65'] = df1[m_ge_45_le_65].sum(axis = 1)
df1 = df1.drop(df1[m_ge_45_le_65], axis = 1)

## 65+
m_ge_65 = ['M65-66', 'M67-69', 'M70-74', 'M76-79', 'M80-84', 'M85+']
df1['male_ge_65'] = df1[m_ge_65].sum(axis = 1)
df1 = df1.drop(df1[m_ge_65], axis = 1)


## FEMALE
## less than 30
f_le_30 = ['W5','W5-9', 'W10-14', 'W15-17', 'W18-19', 'W20', 'W21', 'W22-24', 'W25-29']
df1['female_le_30'] = df1[f_le_30].sum(axis = 1)
df1 = df1.drop(df1[f_le_30], axis = 1)

## 30 - 45
f_ge_30_le_45 = ['W30-34', 'W35-39', 'W40-44']
df1['female_ge_30_le_45'] = df1[f_ge_30_le_45].sum(axis = 1)
df1 = df1.drop(df1[f_ge_30_le_45], axis = 1)

## 45 - 65
f_ge_45_le_65 = ['W45-49', 'W50-54', 'W55-59', 'W60-61', 'W62-64']
df1['female_ge_45_le_65'] = df1[f_ge_45_le_65].sum(axis = 1)
df1 = df1.drop(df1[f_ge_45_le_65], axis = 1)

## 65+
f_ge_65 = ['W65-66', 'W67-69', 'W70-74', 'W76-79', 'W80-84', 'W85+']
df1['female_ge_65'] = df1[f_ge_65].sum(axis = 1)
df1 = df1.drop(df1[f_ge_65], axis = 1)

## join male and female
df1['age_le_30'] = df1['female_le_30'] + df1['male_le_30']
df1['age_ge_30_le_45'] = df1['female_ge_30_le_45'] + df1['male_ge_30_le_45']
df1['age_ge_45_le_65'] = df1['female_ge_45_le_65'] + df1['male_ge_45_le_65']
df1['age_ge_65'] = df1['female_ge_65'] + df1['male_ge_65']


## merge dataframes
df = pd.merge(df1,df2, how='left', on=['NAME','state', 'county', 'fips'])
df = pd.merge(df,df3, how='left', left_on=['fips'], right_on=['FIPS'])


## export as csv
df.to_csv('county_data.csv')
