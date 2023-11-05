from Core import Core
from Plant import Plant
from eto_calc import calculate_ET0
from Database import DatabaseConfig
import requests
from Sensor_management import Sensor


class CoreMenu():
    def __init__(self):
        self.get_url = 'http://127.0.0.1:8000/api/datatable'
        self.update_url = 'http://127.0.0.1:8000/api/datatable/update/'
        self.add_url = 'http://127.0.0.1:8000/api/datatable/add'
        self.api_app = Core()
        self.token = self.get_token()
        self.plants = {}
        self.sensors = []
        self.database = DatabaseConfig(db_name = 'Weather')
        self.database.connect()
        self.core = Core()

    def get_token(self):
        token = input('Please Enter Token: ')
        if self.api_app.is_token_valid(token=token):
            return token
        else:
            print('TOKEN NOT VALID!!!')
            return None

    def add_sensor(self):
        sensor = Sensor(pin=input('enter sensor pin: '), sensor_type=int(input('Enter 0 for moisture sensor or 1 for ph/ec/npk sensor: ')), plant_id=int(input('enter plant_id'))) # change plant_id to come directly without user input
        self.sensors.append(sensor)

    def collect_data(self, sensor_p = None):
        if sensor_p is None:
            for sensor in self.sensors:
                s_data = sensor.collect_data()
                plant_id = sensor.plant_id
                plant = self.database.check_table_id(table_name='PLANT', pk=plant_id)
                if plant:

                    self.core.save_data_measured_plant(plant_name=plant.plant_name, plant_id=plant_id, m_data={'m_moist': s_data})
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
        self.core.sync_data_from_server(token=self.token)






    def run(self):
        pass
start = 'Hello'

menu = CoreMenu()

menu.add_sensor()
menu.get_plant_data()
print(menu.collect_data(sensor_p=1))
