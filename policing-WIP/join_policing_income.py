import pandas as pd
import code
from shapely.geometry import Point, Polygon, MultiPolygon

income_data = pd.read_csv("income_census_tract.csv")
policing_sample = pd.read_csv("policing_sample.csv")

def contained_in(location, location_name, x):
    # the geometry is long, lat for some reason.
    pickup_point = Point(x["Pickup_longitude"], x["Pickup_latitude"])
    dropoff_point = Point(x["Dropoff_longitude"], x["Dropoff_latitude"])
    if location["geometry"].contains(pickup_point)[0]:
        x["pickup_location"] = location_name
    if location["geometry"].contains(dropoff_point)[0]:
        x["dropoff_location"] = location_name
    return x

code.interact(local=locals())
