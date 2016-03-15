from urllib2 import Request, urlopen
import json
import requests
from config import Config
from pandas.io.json import json_normalize

cfg = Config(file('/Users/soniamehta/Desktop/weatherconf.cfg'))

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
"""
cursor.execute(sql)
sql_data = cursor.fetchall()

''' 
This will fetch the data from the API.
'''
lat_long = sql_data
api_key = cfg['WEATHER_KEY']

final_result = []
for item in lat_long:
    coordinates = item['coordinates']
    date = item['invoice_date']
    request=Request('http://api.worldweatheronline.com/free/v2/past-weather.ashx?key='+api_key+coordinates+'"&date="'+date+'"&format=json')
    response = urlopen(request)
    elevations = response.read()
    data = json.loads(elevations)
    results = []
    results.append(coordinates)
    results.append(date)
    results.append(data['data']['weather'][0]['maxtempF'])
    results.append(data['data']['weather'][0]['mintempF'])
    final_result += results

