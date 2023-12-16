# Replace "your_api_key" with your Google API key

import urllib.parse
import requests

main_api = "https://maps.googleapis.com/maps/api/geocode/json?"

key = "your_api_key"

while True:
    address = input("Address: ")

# Add the ability to quit the program.
    if address == "quit" or address == "q":
        break

    url = main_api + urllib.parse.urlencode( {"address": address, "key": key} )
    print(url)

    json_data = requests.get(url).json()
    json_status = json_data["status"]
    print("API Status: " + json_status + "\n")

    if json_status == "OK":
        for each in json_data["results"][0]["address_components"]:
            print(each["long_name"])

        formatted_address = json_data["results"][0]["formatted_address"]
        print("\n" + formatted_address)


'''
OUTPUT:
Address: sjc
https://maps.googleapis.com/maps/api/geocode/json?address=sjc&key='your_api_key'
API Status: OK

Norman Y. Mineta San Jose International Airport
1701
Airport Boulevard
San Jose
Santa Clara County
California
United States
95110

Norman Y. Mineta San Jose International Airport (SJC), 1701 Airport Blvd, San Jose, CA 95110, USA
Address:
'''
