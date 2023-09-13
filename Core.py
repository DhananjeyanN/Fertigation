import mysql.connector
import requests
from datetime import datetime

from Database import DatabaseConfig
import uuid

from Plant import Plant
from test1 import get_django_data


class Core:
    def __init__(self):
        self.api_key = None
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
        print(weather_data)
        self.save_data(weather_data)

    def setup_db(self):
        query = 'CREATE TABLE IF NOT EXISTS FORECAST_WEATHER(row_id INT NOT NULL AUTO_INCREMENT, longitude DECIMAL(10,6),' \
                ' latitude DECIMAL(8,6), date DATETIME, temperature_f DECIMAL(6,2), wind_mph DECIMAL(6,2), ' \
                'pressure_in DECIMAL(6,2), precipitation_in DECIMAL(6,4), humidity INT, ' \
                'cloud INT, dewpoint_f DECIMAL(6,2), chance_rain INT, chance_snow INT, PRIMARY KEY(row_id));'
        self.db.create_table(table_name='Forecast', query=query)

        query2 = 'CREATE TABLE IF NOT EXISTS CURRENT(row_id INT NOT NULL AUTO_INCREMENT, longitude DECIMAL(10,6), ' \
                 'latitude DECIMAL(8,6), date DATETIME, temperature_f DECIMAL(6,2), wind_mph DECIMAL(6,2), ' \
                 'pressure_in DECIMAL(6,2), precipitation_in DECIMAL(6,4), humidity INT,' \
                 'cloud INT, PRIMARY KEY(row_id));'
        self.db.create_table(table_name='Current', query=query2)

        query3 = 'CREATE TABLE IF NOT EXISTS PLANT(row_id INT NOT NULL AUTO_INCREMENT, ' \
                 'PRIMARY KEY(row_id), plant_name VARCHAR(100), ec VARCHAR(100), ph VARCHAR(100), ' \
                 'npk VARCHAR(100), temperature VARCHAR(100), ideal_moisture VARCHAR(100), fertilizer VARCHAR(100), ' \
                 'plant_coefficient DECIMAL(10,6));'
        self.db.create_table(table_name='Plant', query=query3)

        query4 = 'CREATE TABLE IF NOT EXISTS LOCALPLANTDATA(row_id INT NOT NULL AUTO_INCREMENT, ' \
                 'PRIMARY KEY(row_id), plant_name VARCHAR(100), plant_id VARCHAR(1000), m_ec DECIMAL(12,6), m_ph DECIMAL(12,6), ' \
                 'm_npk DECIMAL(12,6), m_temp DECIMAL(12,6), m_moist DECIMAL(12,6), date DATETIME);'
        self.db.create_table(table_name='Localplantdata', query=query4)

    def save_data(self, weather_data):
        current_cols = {
            'lon': 'longitude',
            'lat': 'latitude',
            'temp_f': 'temperature_f',
            'wind_mph': 'wind_mph',
            'pressure_in': 'pressure_in',
            'precip_in': 'precipitation_in',
            'humidity': 'humidity',
            'cloud': 'cloud'
        }
        current_dict = {}
        for key, val in weather_data.items():
            if key == 'current' or 'location':
                for k, v in val.items():
                    if k in current_cols:
                        new_key = current_cols[k]
                        current_dict[new_key] = v
        current_dict['date'] = datetime.now()
        insert_query = "INSERT INTO CURRENT(latitude, longitude, temperature_f, wind_mph, pressure_in, precipitation_in, humidity, cloud, date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        row = list(current_dict.values())
        print(list(current_dict.keys()))
        print(row)
        self.db.insert_data(insert_query, row)

    def save_data_plant(self, plant_data):
        vals = []
        for plant in plant_data:
            print(plant)
            for k, v in plant.items():
                print(k, v)
                if k == 'photo' or k == 'user':
                    pass
                else:
                    print(k, v, 'hi')
                    vals.append(v)
        print(vals)
        try:
            insert_query = "INSERT INTO PLANT(row_id, plant_name, ec, ph, npk, temperature, ideal_moisture, fertilizer, plant_coefficient) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.db.insert_data(insert_query, vals)
        except mysql.connector.IntegrityError:
            pass

    def save_data_measured_plant(self, plant_name, plant_id,
                                 m_data):  # plant_id: send plant unique id, m_data: send dict with name and data
        vals = []
        m_ec = None
        m_ph = None
        m_npk = None
        m_temp = None
        m_moist = None
        date = datetime.now()
        for name, data in m_data.items():
            if name == 'm_ec':
                m_ec = data
            elif name == 'm_ph':
                m_ph = data
            elif name == 'm_npk':
                m_npk = data
            elif name == 'm_temp':
                m_temp = data
            elif name == 'm_moist':
                m_moist = data
            else:
                print('No Data!!!')
        vals.append(plant_name)
        vals.append(plant_id)
        vals.append(m_ec)
        vals.append(m_ph)
        vals.append(m_npk)
        vals.append(m_temp)
        vals.append(m_moist)
        vals.append(date)
        print(vals)
        insert_query = "INSERT INTO LOCALPLANTDATA(plant_name, plant_id ,m_ec, m_ph, m_npk, m_temp, m_moist, date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        self.db.insert_data(insert_query, vals)


# hi = Core()
# hi.get_forecast()

# bean = Plant(hi.db)
# bean.register_plant()
# bean.save_data()
app = Core()
# app.save_data_plant(plant_data=get_django_data())
app.save_data_measured_plant(plant_name='Banana', plant_id="1923", m_data={
    'm_ec': 9.0,
    'm_npk': 3.0,
    'm_ph': 5.0,
    'm_temp': 30.0,
})


def update_plant_details(plant_id, updated_data):
    url = f'http://127.0.0.1:8000/api/update/{plant_id}/'
    token = input('Enter Token')

    # Get CSRF Token

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    response = requests.put(url, json=updated_data, headers=headers)
    print(response.status_code)
    print(response.text)

    return response.json()


# Example usage
plant_id = 1  # Replace with the ID of the plant you want to update
updated_data = {
    'name': 'Updated Bean',
    'ec': '2.5',
    'ph': '3.5',
    'npk': '5',
    'temperature': '25',
    'ideal_moisture': '3',
    'fertilizer': 'Organic',
    'plant_coefficient': 2.5,
    # ... add other fields as necessary
}
print(update_plant_details(plant_id, updated_data))
