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

#printing
print("HOSTS:")
print(get_ticket())
list_host()
print("NETWORK DEVICES:")
list_network_device()

while True:
    s_ip = input("SOURCE: ")
    d_ip = input("DESTINATION: ")
    if s_ip != "" or d_ip != "":
        path_data = {}
        path_data.update(dict(sourceIP=s_ip))
        path_data.update(dict(destIP=d_ip))
        ticket = get_ticket()
        headers = {"content-type": "application/json","X-Auth-Token":ticket}
        api_url = "https://devnetsbx-netacad-apicem-2.cisco.com/api/v1/flow-analysis"
        resp = requests.post(api_url, json.dumps(path_data), headers=headers, verify=False)
        resp_json = resp.json()
        flowAnalysisId = resp_json["response"]["flowAnalysisId"]
        check_url = api_url+"/"+flowAnalysisId
        status = ""
        checks = 0 #variable to increment within the while loop. Will trigger exit from loop after x iterations
        while status != "COMPLETED":
                checks += 1
                r = requests.get(check_url, headers=headers, verify=False)
                response_json = r.json()
                resp_json = response_json
                #+++++++++++Add Values+++++++++++++++
                status = response_json["response"]["request"]["status"] # Assign the value of the status  	of the path trace request from response_json
                #++++++++++++++++++++++++++++++++++++
                
                #wait one second before trying again
                if checks == 15: #number of iterations before exit of loop; change depending on conditions
                        raise Exception("Number of status checks exceeds limit. Possible problem with Path Trace.")
                        #break
                elif status == "FAILED":
                        raise Exception("Problem with Path Trace")
                        #break
                print("REQUEST STATUS: ", status) #Print the status as the loop runs
        networkElementsInfo = resp_json["response"]["networkElementsInfo"]
        for x in networkElementsInfo:
            if "ip" in x:
                print(x["ip"])

    else:
        print("ENTER IP ADDRESS")
        continue
