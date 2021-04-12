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
            "C15002B_006E", #Mbachelor or higher black
            "C15002A_004E", #Mbachelor or higher white
            "C15002C_006E", #Mbachelor or higher native american
            "C15002D_006E", #Mbachelor or higher aapi
            "C15002E_006E", #Mbachelor or higher pacific islander
            "C15002F_006E", #other alone
            "C15002G_006E", #2 or more races
            "C15002B_011E", #Wbachelor or higher white
            "C15002B_011E", #Wbachelor or higher black
            "C15002C_011E", #Wbachelor or higher native american
            "C15002D_011E", #Wbachelor or higher aapi
            "C15002E_006E", #Wbachelor or higher pacific islander
            "C15002F_011E", #Wbachelor or higher other_race_alone
            "C15002G_011E", #Wbachelor or higher 2 or more races
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
            "B19013_001E": "median_income"
            }


data=r.json()
df=pd.DataFrame(data[1:], columns=data[0])

educational_attainment = [
        "C15002B_006E", #Mbachelor or higher black
        "C15002A_004E", #Mbachelor or higher white
        "C15002C_006E", #Mbachelor or higher native american
        "C15002D_006E", #Mbachelor or higher aapi
        "C15002E_006E", #Mbachelor or higher pacific islander
        "C15002F_006E", #other alone
        "C15002G_006E", #2 or more races
        "C15002B_011E", #Wbachelor or higher white
        "C15002B_011E", #Wbachelor or higher black
        "C15002C_011E", #Wbachelor or higher native american
        "C15002D_011E", #Wbachelor or higher aapi
        "C15002E_011E", #Wbachelor or higher pacific islander
        "C15002F_011E", #Wbachelor or higher other_race_alone
        "C15002G_011E" #Wbachelor or higher 2 or more races
]


df[educational_attainment] = df[educational_attainment].apply(pd.to_numeric, axis=1)

df['bachelor_or_higher'] = df[educational_attainment].sum(axis = 1)
df = df.drop(df[educational_attainment], axis = 1)
df=df.rename(columns=rename_cols)
df['fips']=df.state+df.county
df = df.reset_index(drop=True)
df.to_csv('county_demographics.csv')
