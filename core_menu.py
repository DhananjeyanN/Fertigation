from Core import Core
from Plant import Plant
from eto_calc import calculate_ET0
from Database import DatabaseConfig
import requests
from Sensor_management import Sensor
import threading

class CoreMenu():
    def __init__(self):
        self.get_url = 'http://127.0.0.1:8000/api/datatable'
        self.update_url = 'http://127.0.0.1:8000/api/datatable/update/'
        self.add_url = 'http://127.0.0.1:8000/api/datatable/add'
        self.token = self.get_token()
        self.plants = {}
        self.sensors = []
        self.database = DatabaseConfig(db_name = 'Weather')
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

    def add_sensor(self):
        sensor = Sensor(pin=input('enter sensor pin: '), sensor_type=int(input('Enter 0 for moisture sensor or 1 for ph/ec/npk sensor: ')), plant_id=int(input('enter plant_id'))) # change plant_id to come directly without user input
        self.sensors.append(sensor)

    def collect_data(self, sensor_p = None):
        if sensor_p is None:
            for sensor in self.sensors:
                s_data = sensor.collect_data()
                plant_id = sensor.plant_id
                plant = self.database.check_table_id(table_name='PLANT', pk=plant_id)
                print(plant, 'PLANT')
                if plant:

                    self.core.save_data_measured_plant(plant_name=plant[2], plant_id=plant_id,
                                                       m_data={'m_moist': s_data})
                    self.core.sync_data_to_server()
                else:
                    return 'No Plant Found!!!'
        else:
            for sensor in self.sensors:
                if sensor.plant_id == sensor_p:
                    s_data = sensor.collect_data()
                    plant_id = sensor.plant_id
                    plant = self.database.check_table_id(table_name='PLANT', pk=plant_id)
                    print(plant, 'PLANT')
                    if plant:
                        self.core.save_data_measured_plant(plant_name=plant[2], plant_id=plant_id,
                                                           m_data={'m_moist': s_data})
                        self.core.sync_data_to_server()
                    else:
                        return 'No Plant Found!!!'

    def get_plant_data(self):
        self.core.sync_data_from_server()

    def schedule_sync(self, interval=10):
        print(self.collect_data())
        threading.Timer(interval, self.schedule_sync).start()
        print('INTERVAL', interval)

    def run(self):
        self.schedule_sync()






menu = CoreMenu()
menu.get_plant_data()
# menu.add_sensor()
# print(menu.collect_data(sensor_p=1))
menu.run()

