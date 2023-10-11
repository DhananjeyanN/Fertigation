from Core import Core
from Plant import Plant
from eto_calc import calculate_ET0
from Database import DatabaseConfig
import requests


class CoreMenu():
    def __init__(self):
        self.get_url = 'http://127.0.0.1:8000/api/datatable'
        self.update_url = 'http://127.0.0.1:8000/api/datatable/update/'
        self.add_url = 'http://127.0.0.1:8000/api/datatable/add'
        self.api_app = Core()
        self.token = self.get_token()

    def get_token(self):
        token = input('Please Enter Token: ')
        if self.api_app.is_token_valid(token=token):
            return token
        else:
            print('TOKEN NOT VALID!!!')
            return None





    def run(self):
        pass
start = 'Hello'

menu = CoreMenu()

