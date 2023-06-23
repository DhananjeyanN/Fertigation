import requests
from datetime import datetime

from Database import DatabaseConfig


class Core:
    def __init__(self):
        self.api_key = 'dfc94720ef570e3dd395a9ffaf3620bf'
        self.lat = '37.777081'
        self.lon = '-121.967522'

    def get_forecast(self):
        # response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={self.lat} & lon={self.lon}& dt={datetime.now()} & appid = {self.api_key}')
        # print(response.json())
        response = requests.get(
            'https://api.weatherapi.com/v1/forecast.json?key=f2814ffe169642c4a8641448232206&q=94582&days=2&aqi=no&alerts=no')
        weather_data = response.json()
        db = DatabaseConfig()
        db.connect()
        db.create_database('Weather')
        query = 'CREATE TABLE FORECAST WEATHER(row_id INT PRIMARY KEY NOT NULL, longitude DECIMAL(3,6), latitude DECIMAL(3,6), date_time DATETIME, temperature_f DECIMAL(3,2), wind_mph DECIMAL(3,2), gust_mph DECIMAL(3,2), pressure_in DECIMAL(3,2), precipitation_in DECIMAL(3,4), humidity INT, cloud INT, dewpoint_f DECIMAL(3,2), chance_rain INT, chance_snow INT)'
        db.create_table(table_name='Forecast', query=query)
        # query2 = 'CREATE TABLE FORECAST WEATHER(row_id INT PRIMARY KEY NOT NULL, longitude DECIMAL(3,6), ' \
        #          'latitude DECIMAL(3,6), date DATETIME, temperature_f DECIMAL(3,2), wind_mph DECIMAL(3,2), ' \
        #          'gust_mph DECIMAL(3,2), pressure_in DECIMAL(3,2), precipitation_in DECIMAL(3,4), humidity INT, ' \
        #          'cloud INT)'
        # db.create_table(table_name='Current', query=query2)


hi = Core()
hi.get_forecast()
