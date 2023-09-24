from Core import Core
from Plant import Plant
from eto_calc import calculate_ET0
from Database import DatabaseConfig
import requests


class CoreMenu():
    def __init__(self):
        self.token = None
        self.get_url = 'http://127.0.0.1:8000/api/datatable'
        self.update_url = 'http://127.0.0.1:8000/api/datatable/update/'
        self.add_url = 'http://127.0.0.1:8000/api/datatable/add'

    def get_token(self):
        self.token = input('Please Enter Token: ')
        requests.get()

    def run(self):
        self.get_token()
