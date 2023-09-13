import requests

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

# Example usage
entry_id = 1  # Replace with the ID of the DataTable entry you want to update
plant_id = 1  # Replace with the ID of the Plant entry you want to update
updated_data = {
    'plant': plant_id,  # assuming you want to associate this data with a specific plant
    'm_temp': 25.0,
    'm_moist': 3.0,
    'm_ec': 2.5,
    'm_npk': 5.0,
    'm_ph': 3.5,
    # 'date_time': '2023-09-08T12:00:00Z'  # You don't need this for update as it's auto set on creation
}
print(update_data_table_entry(entry_id, updated_data))
