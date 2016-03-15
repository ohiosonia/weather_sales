import os
import MySQLdb
from geopy.geocoders import Nominatim
import pandas as pd

fred_username = os.environ['FRED_USERNAME']
fred_password = os.environ['FRED_PASSWORD']


''' 
This will connect to the database and get a list of the distinct cities and countries.
'''
def connect_db():
    
    return MySQLdb.connect(host="localhost",
                    user=fred_username,
                    passwd=fred_password,
                    db="Chinook")

db = connect_db()
cursor = db.cursor()
sql = """ select DISTINCT concat(BillingCity, ", ", BillingCountry) city_country from invoice"""
cursor.execute(sql)
result_set = cursor.fetchall()
cities = []
for row in result_set:
    cities.append(row[0])


''' 
This will get the latitude and longitude coordinates for all the cities.
'''
lat_long = []
for city in cities:
    geolocator = Nominatim()
    location = geolocator.geocode(city)
    lat_long.append((city, location.latitude, location.longitude))

headers = ["city_country", "latitude", "longitude"]
df = pd.DataFrame(lat_long, columns=headers)
df.to_sql(con=db, name='lat_long', if_exists='replace', flavor='mysql')


