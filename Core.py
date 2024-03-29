import mysql.connector
import requests
from datetime import datetime
from ApiRequests import update_plant_entry, update_data_table_entry, add_data_table_entry
from Database import DatabaseConfig
import uuid

from Plant import Plant
from Sensor_management import Sensor, NPKSensor


class Core:
    def __init__(self, token):
        self.api_key = None
        self.lat = '37.777081'
        self.lon = '-121.967522'
        self.db = DatabaseConfig()
        self.db.connect()
        self.db.create_database('Weather')
        self.setup_db()
        self.token = token

    def get_forecast(self):
        response = requests.get(
            'https://api.weatherapi.com/v1/forecast.json?key=f2814ffe169642c4a8641448232206&q=94582&days=2&aqi=no&alerts=no')
        weather_data = response.json()
        # print(weather_data)
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

        query3 = 'CREATE TABLE IF NOT EXISTS PLANT(plant_id INT NOT NULL UNIQUE, row_id INT NOT NULL AUTO_INCREMENT, ' \
                 'PRIMARY KEY(row_id), plant_name VARCHAR(100), ec VARCHAR(100), ph VARCHAR(100), ' \
                 'nitrogen VARCHAR(100), phosphorus VARCHAR(100), potassium VARCHAR(100), temperature VARCHAR(100), ideal_moisture VARCHAR(100), fertilizer VARCHAR(100), ' \
                 'plant_coefficient DECIMAL(10,6));'
        self.db.create_table(table_name='Plant', query=query3)

        query4 = 'CREATE TABLE IF NOT EXISTS LOCALPLANTDATA(row_id INT NOT NULL AUTO_INCREMENT, uuid VARCHAR(200) NOT NULL UNIQUE, ' \
                 'PRIMARY KEY(row_id), plant_name VARCHAR(100), plant_id INT NOT NULL, m_ec DECIMAL(12,6), m_ph DECIMAL(12,6), ' \
                 'm_nitrogen DECIMAL(12,6), m_phosphorus DECIMAL(12,6), m_potassium DECIMAL(12,6), m_temp DECIMAL(12,6), m_moist DECIMAL(12,6), date DATETIME);'
        self.db.create_table(table_name='Localplantdata', query=query4)

        query5 = 'CREATE TABLE IF NOT EXISTS SENSORS(PRIMARY KEY(plant_id), plant_id INT NOT NULL, sensor_pin INT NOT NULL);'
        self.db.create_table(table_name='Sensor', query=query5)

        query6 = 'CREATE TABLE IF NOT EXISTS NPKSENSOR(current_plant INT, sensor_pin INT NOT NULL);'
        self.db.create_table(table_name='NPKSensor', query=query6)
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
        # print(list(current_dict.keys()))
        # print(row)
        self.db.insert_data(insert_query, row)

    def fetch_plant_data(self, plant_id=None, token=None):
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        if plant_id != None:
            url = f'http://127.0.0.1:8000/api/get_plant/{plant_id}/'
            response = requests.get(url, headers=headers)
            print(response.json())
            response_json = response.json()
            return response_json
        else:
            url = f'http://127.0.0.1:8000/api/get_all_plants/'
            response = requests.get(url, headers=headers)
            response_json = response.json()
            print(response_json)
            if response.status_code == 200:
                response_json = list(response_json)
                plants = []
                plant_fields = ['id', 'name', 'ec', 'ph', 'nitrogen', 'phosphorus', 'potassium', 'temperature', 'ideal_moisture', 'fertilizer',
                                'plant_coefficient', 'user']
                for plant in response_json:
                    new_plant = {}
                    for key in plant.keys():
                        if key in plant_fields:
                            new_plant[key] = plant.get(key)
                    plants.append(new_plant)
                return plants
            else:
                print('NO PLANT FOUND')
                return None

    def db_plant(self, plants):
        self.save_data_plant(plant_data=plants)

    def save_data_plant(self, plant_data):
        for plant in plant_data:
            vals = []
            for k, v in plant.items():
                if k == 'photo' or k == 'user':
                    pass
                else:
                    vals.append(v)
            try:
                insert_query = "INSERT INTO PLANT(plant_id, plant_name, ec, ph, nitrogen, phosphorus, potassium, temperature, ideal_moisture, fertilizer, plant_coefficient) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.db.insert_data(insert_query, vals)
            except mysql.connector.IntegrityError:
                pass

    def save_sensor(self, sensor_data):
        insert_query = "INSERT INTO SENSORS(plant_id, sensor_pin) VALUES(%s,%s)"
        print(insert_query, 'INSERT', sensor_data, 'SENSOR')
        self.db.insert_data(insert_query, sensor_data)

    def save_npk_sensor(self, sensor_data):
        insert_query = "INSERT INTO NPKSENSOR(current_plant, sensor_pin) VALUES(%s,%s)"
        print(insert_query, 'INSERT', sensor_data, 'NPKSENSOR')
        self.db.insert_data(insert_query, sensor_data)

    def save_data_measured_plant(self, plant_name, plant_id, m_data):  # plant_id: send plant unique id, m_data: send dict with name and data
        vals = []
        m_ec = None
        m_ph = None
        m_nitrogen = None
        m_phosphorus = None
        m_potassium = None
        m_temp = None
        m_moist = None
        date = datetime.now()
        for name, data in m_data.items():
            if name == 'ec':
                m_ec = data
            elif name == 'ph':
                m_ph = data
            elif name == 'nitrogen':
                m_nitrogen = data
            elif name == 'phosphorus':
                m_phosphorus = data
            elif name == 'potassium':
                m_potassium = data
            elif name == 'temp':
                m_temp = data
            elif name == 'moisture':
                m_moist = data
            else:
                print('No Data!!!')
        vals.append(str(uuid.uuid4())[:100])
        vals.append(plant_name)
        vals.append(plant_id)
        vals.append(m_ec)
        vals.append(m_ph)
        vals.append(m_nitrogen)
        vals.append(m_phosphorus)
        vals.append(m_potassium)
        vals.append(m_temp)
        vals.append(m_moist)
        vals.append(date)
        insert_query = "INSERT INTO LOCALPLANTDATA(uuid, plant_name, plant_id ,m_ec, m_ph, m_nitrogen, m_phosphorus, m_potassium, m_temp, m_moist, date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.db.insert_data(insert_query, vals)

    def sync_data_to_server(self):
        local_plant_data = self.db.fetch_data('LOCALPLANTDATA')
        print(local_plant_data, 'DADA')
        fields = ['plant_id', 'uuid', 'm_temp', 'm_moist', 'm_ec', 'm_nitrogen', 'm_phosphorus', 'm_potassium', 'm_ph', 'date_time']
        token = self.token
        for p in local_plant_data:
            print(p, 'P')
            p = list(p)
            new_p = []
            del p[0:1]
            new_p.append(p[2])  # plant_id
            new_p.append(p[0])  # uuid
            new_p.append(str(p[8]))  # m_temp
            new_p.append(str(p[9]))  # m_moist
            new_p.append(str(p[3]))  # m_ec
            new_p.append(str(p[5]))  # m_nitrogen
            new_p.append(str(p[6]))  # m_phosphorus
            new_p.append(str(p[7]))  # m_potassium
            new_p.append(str(p[4]))  # m_ph
            new_p.append(str(p[-1]))  # datetime
            print(new_p, 'new_p')
            plant_data = dict(zip(fields, new_p))
            print(plant_data, 'plant_data')
            res = update_data_table_entry(entry_id=plant_data['uuid'], updated_data=plant_data, token=token)
            if res.status_code == 404:
                add_data_table_entry(new_data=plant_data, token=token)

    def sync_data_from_server(self):
        plants = self.db.fetch_data(table_name='PLANT')
        plants_ids = [plant[0] for plant in plants]
        plant_data = self.fetch_plant_data(token=self.token)
        for plant in plant_data:
            vals = []
            for k, v in plant.items():
                if k not in ['photo', 'user']:
                    if k == 'id':
                        if v in plants_ids:
                            plants_ids.remove(v)
                    vals.append(v)
            try:
                insert_query = "INSERT INTO PLANT(plant_id, plant_name, ec, ph, nitrogen, phosphorus, potassium, temperature, ideal_moisture, fertilizer, plant_coefficient) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE plant_name = VALUES(plant_name), ec = VALUES(ec), ph = VALUES(ph), nitrogen = VALUES(nitrogen), phosphorus = VALUES(phosphorus), potassium = VALUES(potassium), temperature = VALUES(temperature), ideal_moisture = VALUES(ideal_moisture), fertilizer = VALUES(fertilizer), plant_coefficient = VALUES(plant_coefficient)"
                self.db.insert_data(insert_query, vals)
            except mysql.connector.Error as e:
                print(f'an error occurred {e}')
        for plant_id in plants_ids:
            self.db.drop_record(record_id=plant_id)

    def is_token_valid(self, token):
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        url = f'http://127.0.0.1:8000/api/get_all_plants/'
        response = requests.get(url, headers=headers)
        response_json = response.json()
        if response.status_code != 200 and response_json['detail'] == 'Given token not valid for any token type':
            return False
        else:
            return True

        # plant_data = self.fetch_plant_data()
        # print(plant_data)
        # self.save_data_plant(plant_data=plant_data)

    def fetch_sensor_data(self):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }
        url = f'http://127.0.0.1:8000/api/get_sensors/'
        response = requests.get(url, headers=headers)
        print(response)
        response_json = response.json()
        print(response_json)
        if response.status_code == 200:
            response_json = list(response_json)
            sensors = []
            print(response_json)
            for sensor in response_json:
                values = list(sensor.values())
                values = [values[-1]] + values[1:3]
                sensors.append(tuple(values))
            print(sensors)
            return sensors
        else:
            print('NO SENSOR FOUND')
            return None

    def fetch_npk_sensor_data(self):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }
        url = f'http://127.0.0.1:8000/api/get_npk_sensor/'
        response = requests.get(url, headers=headers)
        print(response)
        response_json = response.json()
        print(response_json)
        if response.status_code == 200:
            response_json = list(response_json)
            sensor = response_json[0]
            values = list(sensor.values())
            print(values)
            # values = [values[-1]] + values[1:3]
            values = [values[1], values[3]]
            print(values)
            return tuple(values)
        else:
            print('NO SENSOR FOUND')
            return None

    def save_sensor_data(self, sensors):
        for sensor in sensors:
            plant_id, sensor_pin = sensor[1:]
            print(plant_id, 'Plat id')
            print(sensor, 'Sensor')
            if not self.db.fetch_one(query=f'SELECT * FROM SENSORS WHERE plant_id={plant_id}'):
                self.save_sensor(sensor_data=(plant_id, sensor_pin))
                print(f'Sensor {plant_id} Added!!!')
            else:
                print(f'Sensor for {plant_id} exists!!!')

    def save_npk_sensor_data(self, sensor):
        if not self.db.fetch_one(query=f'SELECT * FROM NPKSENSOR'):
            self.save_npk_sensor(sensor_data=sensor)
            print('NPK Sensor Added!!!')
        else:
            print('NPK Sensor exists!!!')

    def load_sensors(self):
        data = self.db.fetch_data(table_name='SENSORS')
        sensors = []
        for row in data:
            sensor = Sensor(pin=row[1], plant_id=row[0])
            sensors.append(sensor)
        return sensors

    def load_npk_sensor(self):
        data = self.db.fetch_data(table_name='NPKSENSOR')
        sensor = NPKSensor(pin=data[1], current_plant=data[0])
        return sensor
    def del_sensor_data(self, plant_id):
        pass
# core = Core(token=' eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjo0ODU5OTMyNTQwLCJpYXQiOjE3MDYzMzI1NDAsImp0aSI6Ijg0ZWZkNjc3NmFhODQ5NjliZTczYzE4MThmYzAwZDEyIiwidXNlcl9pZCI6Mn0.dBvUQyWTW9GyOszqIhqz61ejPvijvqozHCQbfA6qt9A')
# print(core.fetch_npk_sensor_data())
# core = Core(token=' eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjo0ODU1OTU3MjMxLCJpYXQiOjE3MDIzNTcyMzEsImp0aSI6ImEwODc3MzEwYzI5YzQ3M2RhNjI4YWI3ZDY1MzZmMTVhIiwidXNlcl9pZCI6M30.6Vz0v1sViAG43cLphZzba6jEaDeF90W7w3xcaIC_Mdk')
#
# print(core.load_sensors())


# hi = Core()
# hi.get_forecast()

# bean = Plant(hi.db)
# bean.register_plant()
# bean.save_data()
# app = Core()
# # app.save_data_plant(plant_data=get_django_data())
# app.save_data_measured_plant(plant_name='Bean', plant_id="2", m_data={
#     'm_ec': 9.0,
#     'm_nitrogen': 3.0,
#     'm_phosphorus': 2.0,
#     'm_potassium': 1.0,
#     'm_ph': 5.0,
#     'm_temp': 30.0,
# })


# def update_plant_details(plant_id, updated_data):
#     url = f'http://127.0.0.1:8000/api/update/{plant_id}/'
#     token = input('Enter Token')
#
#     # Get CSRF Token
#
#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json',
#     }
#
#     response = requests.put(url, json=updated_data, headers=headers)
#     print(response.status_code)
#     print(response.text)
#
#     return response.json()


# Example usage
# plant_id = 1  # Replace with the ID of the plant you want to update
# updated_data = {
#     'name': 'Updated Bean',
#     'ec': '2.5',
#     'ph': '3.5',
#     'npk': '5',
#     'temperature': '25',
#     'ideal_moisture': '3',
#     'fertilizer': 'Organic',
#     'plant_coefficient': 2.5,
#     # ... add other fields as necessary
# }
# print(update_plant_details(plant_id, updated_data))

# core = Core()
# # print('hello')
# # # core.db_plant(plants=core.fetch_plant_data())
# # # core.sync_data_to_server()
# # # data = core.fetch_plant_data(plant_id=2, token=' eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjo0ODUxNTQ2ODMwLCJpYXQiOjE2OTc5NDY4MzAsImp0aSI6IjdiODc4MDY5ZTczZDRmZTk4Zjc5YzljNmYxMzk2YTVlIiwidXNlcl9pZCI6NH0.UKaNz5_8rSmmuLdEUeguGGuI_TaQx9xhaJ5fMLTsJgY')
# # #
# # # core.save_data_plant(plant_data=[data])
# core.sync_data_to_server()
# core.save_data_measured_plant(plant_name='Banana', plant_id=2, m_data={'m_ec':999, 'm_ph':11, 'm_npk':123})
# core.fetch_plant_data(token=input())