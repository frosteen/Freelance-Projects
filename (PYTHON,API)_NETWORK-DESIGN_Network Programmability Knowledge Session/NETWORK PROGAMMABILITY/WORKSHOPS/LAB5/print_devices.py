import requests
import json
from tabulate import *
from my_apic_em_functions import *

print("LIST OF DEVICES: ")
api_url = "https://devnetsbx-netacad-apicem-1.cisco.com/api/v1/network-device"
ticket = get_ticket()
headers = {
    "content-type": "application/json",
    "X-Auth-Token": ticket
}
resp = requests.get(api_url, headers=headers, verify=False)
if resp.status_code != 200:
    raise Exception("Status code does not equal 200. Response text: " + resp.text)
response_json = resp.json()

device_list = []
i = 0
for item in response_json["response"]:
    i+=1
    device = [ i, item["type"], item["managementIpAddress"] ]
    device_list.append( device )


table_header = ["Number", "Type", "IP"]
print( tabulate(device_list, table_header, tablefmt="fancy_grid") )

input()
