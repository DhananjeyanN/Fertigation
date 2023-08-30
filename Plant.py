from uuid import uuid4
from Database import DatabaseConfig


class Plant:
    def __init__(self,db):
        self.plant_id = None
        self.plant_name = None
        self.ec = None
        self.ph = None
        self.npk = None
        self.temperature = None
        self.moisture = None
        self.db = db
        self.setup_table()
        self.fertilizer = None

    def register_plant(self):
        self.plant_name = input('Enter name of plant: ')
        self.fertilizer = [
            input('Does your plant flower in january'),
            input('Does your plant flower in February'),
            input('Does your plant flower in March'),
            input('Does your plant flower in April'),
            input('Does your plant flower in May'),
            input('Does your plant flower in June'),
            input('Does your plant flower in July'),
            input('Does your plant flower in August'),
            input('Does your plant flower in September'),
            input('Does your plant flower in October'),
            input('Does your plant flower in November'),
            input('Does your plant flower in December'),
        ]
        self.ec = [
            input('Enter the lowest ec concentration for your plant'),
            input('Enter the preferred ec concentration for your plant'),
            input('Enter the highest ec concentration for your plant')
        ]
        self.ph = [
            input('Enter the lowest ph level for your plant'),
            input('Enter the preferred ph level for your plant'),
            input('Enter the highest ph level for your plant')
        ]
        self.npk = [
            input('Enter the lowest nitrogen concentration for your plant'),
            input('Enter the preferred nitrogen concentration for your plant'),
            input('Enter the highest nitrogen concentration for your plant'),

            input('Enter the lowest potassium concentration for your plant'),
            input('Enter the preferred potassium concentration for your plant'),
            input('Enter the highest potassium concentration for your plant'),

            input('Enter the lowest phosphorus concentration for your plant'),
            input('Enter the preferred phosphorus concentration for your plant'),
            input('Enter the highest phosphorus concentration for your plant')
        ]
        self.moisture = [
            input('Enter the lowest moisture level for your plant'),
            input('Enter the preferred moisture level for your plant'),
            input('Enter the highest moisture level for your plant')
        ]
        self.temperature = [
            input('Enter lowest recommended temperature for plant: '),
            input('Enter recommended temperature for plant: '),
            input('Enter highest recommended temperature for plant: '),
        ]

    def read_data(self):
        npk = 1
        ec = 1
        ph = 7
        temperature = 25
        moisture = 30
        return {'NPK': npk, 'EC': ec, 'PH': ph, 'TEMPERATURE': temperature, 'MOISTURE': moisture}

    def setup_table(self):
        query = 'CREATE TABLE IF NOT EXISTS PLANT(plant_id INT NOT NULL AUTO_INCREMENT,' \
                ' plant_name VARCHAR(255), ec VARCHAR(255), ph VARCHAR(255), npk VARCHAR(255),' \
                ' temperature VARCHAR(255), moisture VARCHAR(255), fertilizer VARCHAR(100),PRIMARY KEY(plant_id))'
        self.db.create_table(query=query, table_name='PLANT')

    def save_data(self):
        insert_query = "INSERT INTO PLANT(plant_name, ec, ph, npk, temperature, moisture, fertilizer) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        row = [
            self.plant_name, ','.join(self.ec), ','.join(self.ph), ','.join(self.npk),
            ','.join(self.temperature), ','.join(self.moisture), '.'.join(self.fertilizer)
        ]
        print(type(self.plant_name))
        print(row, insert_query)
        self.db.insert_data(insert_query, row)

    # def water(self):
        
