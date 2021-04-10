import requests
import pandas as pd

HOST = "https://api.census.gov/data"
year = "2019"
dataset = "acs/acs5"
base_url = "/".join([HOST, year, dataset])
predicates = {}


get_vars = ["NAME",
            "B01003_001E", #total
            "B01001_002E", #male
            "B01001_026E", #female
            "B02001_003E", #black
            "B02001_005E", #aapi
            "B02001_007E", #other race alone
            "B03003_003E", #hispanic
            "B19013_001E", #median income
            "C15002B_006E", #Mbachelor or higher
            "C15002B_011E", #Wbachelor or higher
    ]

predicates["get"] = ",".join(get_vars)
predicates["for"] = "county:*"
r = requests.get(base_url, params = predicates)

print(r.text)


rename_cols = {"B01003_001E": "total",
            "B01001_002E": "male",
            "B01001_026E": "female",
            "B02001_003E": "black",
            "B02001_005E": "aapi",
            "B02001_007E": "other_race_alone",
            "B03003_003E": "hispanic",
            "B19013_001E": "median_income",
            "C15002B_006E": "Mbachelor_or_higher",
            "C15002B_011E": "Wbachelor_or_higher"}


data=r.json()
df=pd.DataFrame(data[1:], columns=data[0]).rename(columns=rename_cols)
df['fips']=df.state+df.county
df = df.reset_index(drop=True)
df.to_csv('county_demographics.csv')
