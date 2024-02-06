import sys

from Core import Core
from Plant import Plant
from eto_calc import calculate_ET0
from Database import DatabaseConfig
import requests
from Sensor_management import Sensor, NPKSensor
import threading


class CoreMenu():
    def __init__(self):
        self.get_url = 'http://127.0.0.1:8000/api/datatable'
        self.update_url = 'http://127.0.0.1:8000/api/datatable/update/'
        self.add_url = 'http://127.0.0.1:8000/api/datatable/add'
        self.token = self.get_token()
        self.plants = {}
        self.sensors = []
        self.npksensor = []
        self.database = DatabaseConfig(db_name='Weather')
        self.database.connect()
        self.core = Core(token=self.token)

    def get_token(self):
        token = input('Please Enter Token: ')
        if self.is_token_valid(token=token):
            return token
        else:
            print('TOKEN NOT VALID!!!')
            return None

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

    def add_sensor(self, option=False, o2=0):
        sensor_type = input('Enter 0 for moisture sensor or 1 for npk sensor: ')
        if sensor_type == 0:
            sensor = Sensor(pin=input('enter sensor pin: '), plant_id=int(input('enter plant_id')))
            self.sensors.append(sensor)
        else:
            sensor = NPKSensor(pin=input('enter sensor pin: '), current_plant=int(input('enter plant_id')))
            self.npksensor.append(sensor)
        if option is False and o2 == 0:
            self.core.save_sensor(sensor_data=[sensor.plant_id, sensor.pin])
        elif option is False and o2 == 1:
            self.core.save_npk_sensor(sensor_data=[sensor.current_plant, sensor.pin])

    def collect_data(self, sensor_p=None):
        if sensor_p is None:
            for sensor in self.sensors:
                s_data = sensor.collect_data()
                print(s_data, 'sdata')
                plant_id = sensor.plant_id
                plant = self.database.check_table_id(table_name='PLANT', pk=plant_id)
                print(plant, 'PLANTT')
                if plant:

                    self.core.save_data_measured_plant(plant_name=plant[2], plant_id=plant_id,
                                                       m_data=s_data)
                    self.core.sync_data_to_server()
                else:
                    return 'No Plant Found!!!'
        else:
            for sensor in self.sensors:
                if sensor.plant_id == sensor_p:
                    s_data = sensor.collect_data()
                    plant_id = sensor.plant_id
                    plant = self.database.check_table_id(table_name='PLANT', pk=plant_id)
                    if plant:
                        self.core.save_data_measured_plant(plant_name=plant[2], plant_id=plant_id, m_data={'m_moist': s_data})
                        self.core.sync_data_to_server()
                    else:
                        return 'No Plant Found!!!'

    def collect_data_npk(self):
        s_data = self.npksensor[0].collect_data()
        current_plant_id = self.npksensor[0].current_plant
        current_plant = self.database.check_table_id(table_name='PLANT', pk=current_plant_id)
        if current_plant:
            self.core.save_data_measured_plant(plant_name=current_plant[2], plant_id=current_plant_id, m_data=s_data)

    def get_plant_data(self):
        self.core.sync_data_from_server()

    def schedule_sync(self, interval=10):
        print(self.collect_data())
        print(self.collect_data_npk())
        self.core.sync_data_from_server()
        self.core.sync_data_to_server()
        self.core.save_sensor_data(sensors=self.core.fetch_sensor_data())
        self.core.save_npk_sensor_data(sensor=self.core.fetch_npk_sensor_data())
        threading.Timer(interval, self.schedule_sync).start()
        print('INTERVAL', interval)

    def run(self):
        sensors = self.database.fetch_data('SENSORS')
        for sensor in sensors:
            print(sensor)
            self.sensors.append(Sensor(pin=sensor[1], plant_id=sensor[0]))
        npk_sensor = self.database.fetch_data('NPKSENSOR')
        print(list(npk_sensor[0]), 'HELLO')
        npk_sensor = list(npk_sensor[0])
        self.npksensor.append(NPKSensor(pin=npk_sensor[1], current_plant=npk_sensor[0]))
        print(self.sensors)
        print(self.npksensor)
        self.schedule_sync()


menu = CoreMenu()
menu.get_plant_data()
# print(menu.collect_data(sensor_p=1))
menu.run()
