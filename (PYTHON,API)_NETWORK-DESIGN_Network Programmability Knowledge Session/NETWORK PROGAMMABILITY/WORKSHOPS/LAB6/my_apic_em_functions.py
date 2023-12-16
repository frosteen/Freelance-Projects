import json
import requests
from tabulate import *
from get_colors import color
requests.packages.urllib3.disable_warnings()

def get_ticket():
    api_url = "https://devnetsbx-netacad-apicem-2.cisco.com/api/v1/ticket"
    headers = {
        "content-type": "application/json"
    }
    body_json = {
        "username": "devnetuser",
        "password": "w0ISNW79"
    }
    resp=requests.post(api_url,json.dumps(body_json),headers=headers,verify=False)
    response_json = resp.json()
    serviceTicket = response_json["response"]["serviceTicket"]
    return serviceTicket


def print_hosts():
    api_url = "https://devnetsbx-netacad-apicem-1.cisco.com/api/v1/host"
    ticket = get_ticket()
    headers = {
        "content-type": "application/json",
        "X-Auth-Token": ticket
    }
    resp = requests.get(api_url, headers=headers, verify=False)
    if resp.status_code != 200:
        raise Exception("Status code does not equal 200. Response text: " + resp.text)
    response_json = resp.json()
    host_list = []
    i = 0
    for item in response_json["response"]:
        i+=1
        host = [
                i,
                item["hostType"],
                item["hostIp"] ,
                item["hostMac"] 
                ]
        host_list.append( host )

    table_header = ["Number", "Type", "IP", "Mac-Address"]
    print(color.BOLD+ tabulate(host_list, table_header, tablefmt="fancy_grid") +color.END)
    return host_list

def print_devices():
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
        device = [ i, item["type"], item["managementIpAddress"], item["macAddress"] ]
        device_list.append( device )


    table_header = ["Number", "Type", "IP", "Mac-Address"]
    print(color.BOLD+ tabulate(device_list, table_header, tablefmt="fancy_grid") +color.END)
    return device_list

