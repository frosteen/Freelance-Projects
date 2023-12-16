# Replace "your_api_key" with your Google API key

import urllib
import requests

main_api = "https://maps.googleapis.com/maps/api/geocode/json?"
key = "your_key_here"

while True:
    address = input("Address: ")
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
