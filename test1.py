import requests
from Core import Core

def get_data_table_entries():
    url = 'http://127.0.0.1:8000/api/datatable'
    token = input('Enter Token')
    data = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    print(data.json())
    return data.json()

def update_data_table_entry(entry_id, updated_data):
    url = f'http://127.0.0.1:8000/api/datatable/update/{entry_id}/'  # Assuming this is your endpoint
    token = input('Enter Token')

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    response = requests.put(url, json=updated_data, headers=headers)
    print(response.status_code)
    print(response.text)

    return response.json()


def add_data_table_entry(new_data):
    url = f'http://127.0.0.1:8000/api/datatable/add/'  # Assuming this is your endpoint
    token = input('Enter Token')

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    response = requests.post(url, json=new_data, headers=headers)
    print(response.status_code)
    print(response.text)
    if response.status_code == 201:
        return response.json()
    else:
        print(response.text)


def del_data_table_entry(entry_id):
        url = f'http://127.0.0.1:8000/api/datatable/del/{entry_id}/'  # Assuming this is your endpoint
        token = input('Enter Token')

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

        response = requests.delete(url, headers=headers)
        print(response.status_code)
        print(response.text)
        if response.status_code == 204:
            return {'message': 'deleted succesfully!!!'}
        else:
            return response.text


# def get_user_plant_data(plant_id):
#     url = f'http://127.0.0.1:8000/api/get_plant/{plant_id}/'
#     token = input('Enter token: ')
#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json',
#     }
#     response = requests.get(url, headers=headers)
#     print(response.json())
#     response_json = response.json()
#     plant_name = response_json.get('name')
#     plant_id = response_json.get('id')
#     core = Core()
#     core.save_data_measured_plant(plant_name=plant_name, plant_id=plant_id)




# Example usage
# entry_id = 2  # Replace with the ID of the DataTable entry you want to update
# plant_id = 1  # Replace with the ID of the Plant entry you want to update
# updated_data = {
#     'plant': plant_id,  # assuming you want to associate this data with a specific plant
#     'm_temp': 29.0,
#     'm_moist': 23.0,
#     'm_ec': 4.5,
#     'm_npk': 2.0,
#     'm_ph': 1.5,
#     # 'date_time': '2023-09-08T12:00:00Z'  # You don't need this for update as it's auto set on creation
# }
# print(update_data_table_entry(entry_id, updated_data))

# plant_id = 1  # Replace with the ID of the Plant entry you want to update
# new_data = {
#     'plant': plant_id,  # assuming you want to associate this data with a specific plant
#     'm_temp': 1.0,
#     'm_moist': 90.0,
#     'm_ec': 9.2,
#     'm_npk': 3.0,
#     'm_ph': 2.5,
#     # 'date_time': '2023-09-08T12:00:00Z'  # You don't need this for update as it's auto set on creation
# }
# print(add_data_table_entry(new_data))

# print(del_data_table_entry(entry_id=8))
get_user_plant_data(plant_id=1)