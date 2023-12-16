import urllib
import requests
from parsingJson import key
from get_colors import color
import os


os.system("cls")
main_api = "https://maps.googleapis.com/maps/api/geocode/json?"
address = "san jose"
key = key.primaryKey

url = main_api + urllib.urlencode({"address": address, "key": key})

json_data = requests.get(url).json()
while True:
    print(color.GREEN+"GEOCODE API:"+color.END)
    print(color.CYAN+"*Type 'quit' or 'q' to exit the program."+color.END)
    address = raw_input("Input any address: ")
    
    if address == "quit" or address == "q":
        break
    
    url = main_api + urllib.urlencode({"address": address, "key": key})
    #print(url)

    json_data = requests.get(url).json()
    json_status = json_data["status"]
    print("API Status: " + json_status)

    if json_status == "OK":
        print(color.BOLD+"LONG NAME:"+color.END)
        for each in json_data["results"][0]["address_components"]:
            print(each["long_name"])

        print(color.BOLD+"FORMATTED ADDRESS:"+color.END)
        formatted_address = json_data["results"][0]["formatted_address"]
        print(formatted_address)


