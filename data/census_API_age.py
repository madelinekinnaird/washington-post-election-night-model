import requests
import pandas as pd

HOST = "https://api.census.gov/data"
year = "2019"
dataset = "acs/acs5"
base_url = "/".join([HOST, year, dataset])
predicates = {}


get_vars = ["NAME",
            "B01001_001E", #total (age)
            "B01001_002E", #M5
            "B01001_003E", #M5-9
            "B01001_004E", #M10-14
            "B01001_006E", #M15-17
            "B01001_007E", #M18-19
            "B01001_008E", #M20
            "B01001_009E", #M21
            "B01001_010E", #M22-24
            "B01001_011E", #M25-29
            "B01001_012E", #M30-34
            "B01001_013E", #M35-39
            "B01001_014E", #M40-44
            "B01001_015E", #M45-49
            "B01001_016E", #M50-54
            "B01001_017E", #M55-59
            "B01001_018E", #M60-61
            "B01001_019E", #M62-64
            "B01001_020E", #M65-66
            "B01001_021E", #M67-69
            "B01001_022E", #M70-74
            "B01001_023E", #M76-79
            "B01001_024E", #M80-84
            "B01001_025E", #M85+
            "B01001_027E", #W5
            "B01001_028E", #W5-9
            "B01001_029E", #W10-14
            "B01001_030E", #W15-17
            "B01001_031E", #W18-19
            "B01001_032E", #W20
            "B01001_033E", #W21
            "B01001_034E", #W22-24
            "B01001_035E", #W25-29
            "B01001_036E", #W30-34
            "B01001_037E", #W35-39
            "B01001_038E", #W40-44
            "B01001_039E", #W45-49
            "B01001_040E", #W50-54
            "B01001_041E", #W55-59
            "B01001_042E", #W60-61
            "B01001_043E", #W62-64
            "B01001_044E", #W65-66
            "B01001_045E", #W67-69
            "B01001_046E", #W70-74
            "B01001_047E", #W76-79
            "B01001_048E", #W80-84
            "B01001_049E", #W85+
]

predicates["get"] = ",".join(get_vars)
predicates["for"] = "county:*"
r = requests.get(base_url, params = predicates)

print(r.text)

data=r.json()
df=pd.DataFrame(data[1:], columns=data[0])#.\
    #rename(columns={"NATURALINC": "Natural Increase", "DOMESTICMIG": "Net Domestic Mig", "INTERNATIONALMIG":"Net Foreign Mig"})
df['fips']=df.state+df.county
df.set_index('fips', inplace=True)
df.drop(columns=['state','county'], inplace=True)
df=df.astype(dtype={'Natural Increase':'int64','Net Domestic Mig':'int64','Net Foreign Mig':'int64'},inplace=True)
df


## export df as csv
