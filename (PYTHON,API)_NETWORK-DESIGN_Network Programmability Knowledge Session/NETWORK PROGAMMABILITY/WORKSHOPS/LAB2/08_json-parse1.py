import urllib
import requests
from parsingJson import key

main_api = "https://maps.googleapis.com/maps/api/geocode/json?"
address = "san jose"
key = key.primaryKey

url = main_api + urllib.urlencode({"address": address, "key": key})
print(url)
json_data = requests.get(url).json()
print(json_data)
