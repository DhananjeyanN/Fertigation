import random


class Sensor:
    def __init__(self, pin=None, plant_id=None):
        self.pin = pin
        self.plant_id = plant_id
        self.valid_range = {'moisture': [0, 100]}

    def collect_data(self):
        return {'moisture': random.randint(a=self.valid_range['moisture'][0], b=self.valid_range['moisture'][1])}


class NPKSensor:
    def __init__(self, pin, current_plant):
        self.pin = pin
        self.current_plant = current_plant
        self.valid_range = {'ph': [0, 14], 'ec': [0, 1000], 'nitrogen': [0, 500], 'phosphorus': [0, 500],
                            'potassium': [0, 500]}  # ph, ec, npk

    def collect_data(self):
        return {'ph': random.randint(a=self.valid_range['ph'][0], b=self.valid_range['ph'][1]),
                'ec': random.randint(a=self.valid_range['ec'][0], b=self.valid_range['ec'][1]),
                'nitrogen': random.randint(a=self.valid_range['nitrogen'][0], b=self.valid_range['nitrogen'][1]),
                'phosphorus': random.randint(a=self.valid_range['phosphorus'][0], b=self.valid_range['phosphorus'][1]),
                'potassium': random.randint(a=self.valid_range['potassium'][0], b=self.valid_range['potassium'][1])}





# sensor = Sensor(sensor_type=1)
# print(sensor.collect_data())