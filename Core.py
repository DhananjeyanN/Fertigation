import requests
from datetime import datetime

from Database import DatabaseConfig


class Core:
    def __init__(self):
        self.api_key = 'dfc94720ef570e3dd395a9ffaf3620bf'
        self.lat = '37.777081'
        self.lon = '-121.967522'
        self.db = DatabaseConfig()
        self.db.connect()
        self.db.create_database('Weather')
        self.setup_db()

    def get_forecast(self):
        response = requests.get(
            'https://api.weatherapi.com/v1/forecast.json?key=f2814ffe169642c4a8641448232206&q=94582&days=2&aqi=no&alerts=no')
        weather_data = response.json()
        self.save_data(weather_data)

    def setup_db(self):
        query = 'CREATE TABLE IF NOT EXISTS FORECAST_WEATHER(row_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, longitude DECIMAL(6,6),' \
                ' latitude DECIMAL(6,6), date_time DATETIME, temperature_f DECIMAL(3,2), wind_mph DECIMAL(3,2), ' \
                'pressure_in DECIMAL(3,2), precipitation_in DECIMAL(4,4), humidity INT, ' \
                'cloud INT, dewpoint_f DECIMAL(3,2), chance_rain INT, chance_snow INT)'
        self.db.create_table(table_name='Forecast', query=query)

        query2 = 'CREATE TABLE IF NOT EXISTS CURRENT(row_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, longitude DECIMAL(6,6), ' \
                 'latitude DECIMAL(6,6), date DATETIME, temperature_f DECIMAL(3,2), wind_mph DECIMAL(3,2), ' \
                 'pressure_in DECIMAL(3,2), precipitation_in DECIMAL(4,4), humidity INT, ' \
                 'cloud INT)'
        self.db.create_table(table_name='Current', query=query2)

    def save_data(self, weather_data):
        current_cols = {
            'lon':'longitude',
            'lat':'latitude',
            'temp_f':'temperature_f',
            'wind_mph':'wind_mph',
            'pressure_in':'pressure_in',
            'precip_in':'precipitation_in',
            'humidity':'humidity',
            'cloud':'cloud'
        }
        current_dict = {}
        for key, val in weather_data.items():
            if key == 'current' or 'location':
                for k,v in val.items():
                    if k in current_cols:
                        new_key = current_cols[k]
                        current_dict[new_key] = v
        current_dict['date'] = datetime.now()
        print(current_dict)
        insert_query = "INSERT INTO CURRENT('latitude', 'longitude', 'temperature_f', 'wind_mph', 'pressure_in', 'precipitation_in', 'humidity', 'cloud', 'date') VALUES(?,?,?,?,?,?,?,?,?)"
        print(len(current_dict.values()))
        row = list(current_dict.values())
        print(current_dict.keys())
        self.db.insert_data(insert_query, row)


hi = Core()
hi.get_forecast()
