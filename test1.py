import requests


def get_django_data():
    url1 = 'http://127.0.0.1:8000/plants'
    url2 = 'http://127.0.0.1:8000/datatable'
    token = input('Enter Token')
    data1= requests.get(url1, headers={'Authorization': f'Bearer {token}'})
    # data2 = requests.get(url2, headers={'Authorization': f'Bearer {token}'})
    print(data1.json())
    # print(data2.json())
    return data1.json()


# get_django_data()
