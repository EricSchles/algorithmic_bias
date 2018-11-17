import pandas as pd
from functools import partial
import code

def get_tract(x):
    return x["geo_name"].split(" ")[-1]

def select_tracts(listing, x):
    if x["tract"] in listing:
        return True
    else:
        return False

def census_tracts_transform(census_tracts):
    tracts = list(census_tracts["TRACT"].unique())
    new_tracts = []
    for tract in tracts:
        if len(str(tract)) == 3:
            new_tracts.append(
                "0"+str(tract)
            )
        else:
            new_tracts.append(
                str(tract)
            )
    return new_tracts

def census_tracts_transform_col(census_tracts):
    tracts = census_tracts["TRACT"]
    new_tracts = []
    for tract in tracts:
        if len(str(tract)) == 3:
            new_tracts.append(
                "0"+str(tract)
            )
        else:
            new_tracts.append(
                str(tract)
            )
    census_tracts["TRACT"] = new_tracts
    return census_tracts
 

census_tracts = pd.read_csv("Austin_Census_Tracts_9Gg.csv")
income = pd.read_csv("Data USA Cart.csv")
income = income[["geo_name", "income_2015"]]

income.dropna(inplace=True)
income["tract"] = income.apply(get_tract, axis=1)

census_tracts_list = census_tracts_transform(census_tracts)
tract_select = partial(select_tracts, census_tracts_list)
booleans = income.apply(tract_select, axis=1)
new_income = income[booleans]
census_tracts = census_tracts_transform_col(census_tracts)

the_geoms = []
for income_idx in new_income.index:
    tract = new_income.loc[income_idx]["tract"]
    the_geoms.append(census_tracts[census_tracts["TRACT"] == tract]["the_geom"])
new_income["census_polygon"] = the_geoms

new_income.to_csv("income_census_tract.csv")
        
