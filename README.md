# weather_sales


The purpose of this repository is to see if there are correlations between the
Chinook sales and the weather.

The scripts are not complete, however the general framework of how to do this
is listed below.

Step 1: get_latitude_longitude.py

This script connects to the database and takes each of the cities provided in 
the Invoice table and gets the city's longitude and latitude. The API key in
the .cfg file has been removed, for security reasons.

Step 2: get_data_from_api.py

This script takes the invoice dates and longitude and latitude coordinates and
polls the API for the high and low temperature that day. This script is 
incomplete. This script needs to put the data into a dataframe.

Step 3: Find correlations
This has not been completed. However, in order to understand if correlations
occurred between the sales data and the weather, I would use a correlation
matrix. I would also plot the sales totals against the high and low 
temperatures using matplotlib, to visually see if there are any correlations.

If correlations do not exist, then I will try to expand the weather data, to
see if I can get more qualitative information about the weather -- did it rain,
snow, etc. that day and then dummify those variables to create a linear
regression. From there, I would look at the Rsquared value and see how well the
model was able to predict the sales, based off weather.
