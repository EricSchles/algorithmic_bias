import pandas as pd
import requests
import json

def census_query_formatting(street, city, state):
    street = "+".join(street.split(" "))
    city = "+".join(city.split(" "))
    prepend = "https://geocoding.geo.census.gov/geocoder/locations/address?"
    address = "street={}&city={}&state={}".format(street, city, state)
    postpend = "&benchmark=Public_AR_Census2010&format=json"
    return prepend+address+postpend

def google_query_formatting(street, city, state):
    street = "+".join(street.split(" "))
    prepend = "https://maps.googleapis.com/maps/api/geocode/json?"
    address="address={},{},{}&".format(street, city, state)
    postpend = "key=" # Google API goes here
    return prepend+address+postpend

def geocoding(street, city, state, query_format):
    if "census" == query_format:
        query_string = census_query_formatting(street, city, state)
    elif "google" == query_format:
        query_string = google_query_formatting(street, city, state)
    return requests.get(query_string).json()

def address_to_latlong(street):
    try:
        geojson_object = geocoding(street, "Austin", "TX", "census")
        result = geojson_object["result"]["addressMatches"]
        if result != []:
            return result[0]["coordinates"]["y"], result[0]["coordinates"]["x"]
        else:
            result = geocoding(street, "Austin", "TX", "google")
            return result["results"][0]["geometry"]["location"]["lat"], result["results"][0]["geometry"]["location"]["lng"]
    except:
        result = geocoding(street, "Austin", "TX", "google")
        return result["results"][0]["geometry"]["location"]["lat"], result["results"][0]["geometry"]["location"]["lng"]

df = pd.read_csv("Racial_Profiling_Dataset_2015_Citations.csv")        
lats = []
longs = []
sample = df[:3000]

successful_indices = []
for i in range(len(sample)):
    try:
        result = address_to_latlong(sample["VL STREET NAME"][i])
        lats.append(result[0])
        longs.append(result[1])
        successful_indices.append(i)
    except:
        continue
if successful_indices != list(range(3000)):
    sample = sample.iloc[successful_indices]
    
sample["latitude"] = lats
sample["longitude"] = longs
sample.to_csv("policing_sample.csv")
