import os
import MySQLdb
from urllib2 import Request, urlopen
import json
import requests
from config import Config
# from pandas.io.json import json_normalize

fred_username = os.environ['FRED_USERNAME']
fred_password = os.environ['FRED_PASSWORD']

cfg = Config(file('/Users/soniamehta/Desktop/weather_sales/weatherconf.cfg'))

''' 
This will connect to the database.
'''
def connect_db():
    
    return MySQLdb.connect(host="localhost",
                    user=fred_username,
                    passwd=fred_password,
                    db="Chinook")

db = connect_db()

''' 
This will get the latitude and longitude coordinates and the dates for all invoice dates from MySQL.
'''
sql = """
SELECT      cast(DATE(InvoiceDate) AS CHAR) invoice_date
            , BillingCity
            , BillingCountry
            , concat(latitude, ",", longitude) coordinates
            , latitude
            , longitude
            , sum(Total) total_sales
FROM        invoice inv
JOIN        lat_long latlong
ON          latlong.city_country = concat(inv.BillingCity, ", ", inv.BillingCountry)
GROUP BY    cast(DATE(InvoiceDate) AS CHAR), BillingCity, BillingCountry, latitude, longitude
LIMIT       5
"""
cursor = db.cursor()
cursor.execute(sql)
sql_data = cursor.fetchall()

''' 
This will fetch the data from the API.
'''
lat_long = sql_data
lat_long = [list(x) for x in lat_long]
api_key = cfg['WEATHER_KEY']


final_result = []
for item in lat_long:
    coordinates = item[3]
    date = item[0]
    billingcity = item[1]
    billingcountry = item[2]
    request=Request('http://api.worldweatheronline.com/free/v2/past-weather.ashx?key='+api_key+'&q="'+coordinates+'"&date="'+date+'"&format=json')
    response = urlopen(request)
    elevations = response.read()
    data = json.loads(elevations)
    results = []
    dictResult = {}
    dictResult['billingcity'] = billingcity
    dictResult['billingcountry'] = billingcountry 
    dictResult['coordinates'] = coordinates
    dictResult['date'] = date
    dictResult['max'] = data['data']['weather'][0]['maxtempF']
    dictResult['min'] = data['data']['weather'][0]['mintempF']
    results.append(dictResult)
    final_result += results
