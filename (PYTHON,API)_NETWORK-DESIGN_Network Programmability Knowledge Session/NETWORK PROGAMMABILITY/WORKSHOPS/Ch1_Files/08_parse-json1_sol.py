# Replace "your_api_key" with your Google API key

from urllib import parse
import requests

main_api = "https://maps.googleapis.com/maps/api/geocode/json?"
address = "san jose"
key = "your_api_key"

url = main_api + urllib.parse.urlencode( {"address": address, "key": key} )

json_data = requests.get(url).json()
print(json_data)

'''
OUTPUT:
{'status': 'OK', 'results': [{'types': ['locality', 'political'], 'formatted_address': 'San Jose, CA, USA', 'geometry': {'bounds': {'northeast': {'lat': 37.4695381, 'lng': -121.589154}, 'southwest': {'lat': 37.124493, 'lng': -122.0456719}}, 'viewport': {'northeast': {'lat': 37.4695381, 'lng': -121.589154}, 'southwest': {'lat': 37.124493, 'lng': -122.0456719}}, 'location_type': 'APPROXIMATE', 'location': {'lat': 37.3382082, 'lng': -121.8863286}}, 'address_components': [{'long_name': 'San Jose', 'types': ['locality', 'political'], 'short_name': 'San Jose'}, {'long_name': 'Santa Clara County', 'types': ['administrative_area_level_2', 'political'], 'short_name': 'Santa Clara County'}, {'long_name': 'California', 'types': ['administrative_area_level_1', 'political'], 'short_name': 'CA'}, {'long_name': 'United States', 'types': ['country', 'political'], 'short_name': 'US'}], 'place_id': 'ChIJ9T_5iuTKj4ARe3GfygqMnbk'}]}
>>>
'''
