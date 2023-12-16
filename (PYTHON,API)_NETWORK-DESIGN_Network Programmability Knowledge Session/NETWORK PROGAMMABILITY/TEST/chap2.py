import json
import requests
from tabulate import tabulate
requests.packages.urllib3.disable_warnings()

def get_ticket():
    api_url = "https://devnetsbx-netacad-apicem-2.cisco.com/api/v1/ticket"
    headers = {"content-type": "application/json"}
    body_json = {
      "username": "devnetuser",
      "password": "w0ISNW79"
    }
    resp = requests.post(api_url,json.dumps(body_json), headers=headers, verify=False)
    response_json = resp.json()
    return (response_json["response"]["serviceTicket"])

def list_host():
    api_url = "https://devnetsbx-netacad-apicem-2.cisco.com/api/v1/host"
    ticket = get_ticket()
    headers = {"content-type": "application/json","X-Auth-Token":ticket}
    resp = requests.get(api_url, headers=headers, verify=False)
    reponse_json = resp.json()
    host_list = []
    i = 0
    for item in reponse_json["response"]:
        i+=1
        host = [i,item["hostType"], item["hostIp"]]
        host_list.append(host)
    table_header = ["Number", "Type", "IP"]
    print(tabulate(host_list,table_header))

def list_network_device():
    api_url = "https://devnetsbx-netacad-apicem-2.cisco.com/api/v1/network-device"
    ticket = get_ticket()
    headers = {"content-type": "application/json","X-Auth-Token":ticket}
    resp = requests.get(api_url, headers=headers, verify=False)
    reponse_json = resp.json()
    network_list = []
    i = 0
    for item in reponse_json["response"]:
        i+=1
        network = [i,item["type"], item["managementIpAddress"]]
        network_list.append(network)
    table_header = ["Number", "Type", "IP"]
    print(tabulate(network_list,table_header))



