
class Plant:
    def __init__(self):
        self.name = None
        self.ec = None
        self.ph = None
        self.npk = None
        self.temperature = None
        self.moisture = None
        self.fertilizer = None

    def register_plant(self):
        self.name = input('Enter name of plant: ')
        self.fertilizer = {
            'January' :input('Does your plant flower in january'),
            'February' :input('Does your plant flower in February'),
            'March' :input('Does your plant flower in March'),
            'April' :input('Does your plant flower in April'),
            'May' :input('Does your plant flower in May'),
            'June' :input('Does your plant flower in June'),
            'July' :input('Does your plant flower in July'),
            'August' :input('Does your plant flower in August'),
            'September' :input('Does your plant flower in September'),
            'October': input('Does your plant flower in October'),
            'November' :input('Does your plant flower in November'),
            'December': input('Does your plant flower in December'),
        }
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
        return {'NPK' :npk, 'EC' :ec, 'PH' :ph, 'TEMPERATURE': temperature, 'MOISTURE' :moisture}
