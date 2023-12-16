import urllib
import requests
from parsingJson import key

main_api = "https://maps.googleapis.com/maps/api/geocode/json?"
address = "san jose"
key = key.primaryKey

url = main_api + urllib.urlencode({"address": address, "key": key})

json_data = requests.get(url).json()
while True:
    address = raw_input("Address: ")
    
    url = main_api + urllib.urlencode({"address": address, "key": key})
    print(url)

    json_data = requests.get(url).json()
    json_status = json_data["status"]
    print("API Status: " + json_status)

    if json_status == "OK":
        formatted_address = json_data["results"][0]["formatted_address"]
        print(formatted_address)

