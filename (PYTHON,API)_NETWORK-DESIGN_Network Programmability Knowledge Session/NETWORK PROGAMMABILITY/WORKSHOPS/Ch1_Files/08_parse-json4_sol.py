# Replace "your_api_key" with your Google API key

import urllib.parse
import requests

main_api = "https://maps.googleapis.com/maps/api/geocode/json?"
key = "your_api_key"

while True:
    address = input("Address: ")

    url = main_api + urllib.parse.urlencode( {"address": address, "key": key} )
    print(url)

    json_data = requests.get(url).json()
    json_status = json_data["status"]
    print("API Status: " + json_status)

    formatted_address = json_data["results"][0]["formatted_address"]
    print(formatted_address)

'''
OUTPUT:
Address: sjc
https://maps.googleapis.com/maps/api/geocode/json?address=sjc&key='your_api_key'
API Status: OK
Norman Y. Mineta San Jose International Airport (SJC), 1701 Airport Blvd, San Jose, CA 95110, USA
Address: lax
https://maps.googleapis.com/maps/api/geocode/json?address=lax&key=your_api_key'
API Status: OK
Los Angeles International Airport (LAX), 1 World Way, Los Angeles, CA 90045, USA
Address:
'''
