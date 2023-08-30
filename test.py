import requests

response = requests.get(
    'https://developer.nrel.gov/api/solar/solar_resource/v1.json?limit=1&lat=37.7534711&lon=-121.8933363&api_key=TgdrTqKE8podlbgx4fp2FJuEk76X6FVcuf957dn8')
weather_data = response.json()
print(weather_data)