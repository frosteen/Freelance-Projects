import json
import requests
from tabulate import *
from my_apic_em_functions import *
from get_colors import color

def doPathTrace():
    print(color.BOLD+"PATH TRACE SIMULATION:"+color.END)

    requests.packages.urllib3.disable_warnings()

    api_url = "https://devnetsbx-netacad-apicem-1.cisco.com/api/v1/flow-analysis"
    ticket = get_ticket()
    headers = {
        "content-type": "application/json",
        "X-Auth-Token": ticket
    }
    resp = requests.get(api_url, headers=headers, verify=False)
    if resp.status_code != 200:
        raise Exception("Status code does not equal 200. Response text: " + resp.text)
    response_json = resp.json()

    print(color.BOLD+"LIST OF HOSTS:"+color.END)
    apiHosts = print_hosts()
    print(color.BOLD+"LIST OF NETWORK DEVICES:"+color.END)
    apiDevices = print_devices()

    path_data = {}
    allAddress = []
    for v in apiHosts:
        allAddress.append(v[2])
    for v in apiDevices:
        allAddress.append(v[2])

    def pathTrace():
        printError = color.RED+"Not a valid ip Address."+color.END
        s_ip = raw_input("Input Source IP Address: ")
        d_ip = raw_input("Input Destination IP Address: ")
        splits_ip = s_ip.split(".")
        splitd_ip = s_ip.split(".")
        if len(splits_ip) == 4 and len(splits_ip) == 4:
            try:
                for x in splits_ip:
                    x = int(x)
                for y in splitd_ip:
                    y = int(y)
            except:
                print(printError)
                pathTrace()
            if not s_ip in allAddress or not d_ip in allAddress:
                print(color.RED+"Some IP address is not found in the list."+color.END)
                pathTrace()
            
            path_data.update(dict(sourceIP=s_ip))
            path_data.update(dict(destIP=d_ip))
            resp = requests.post(api_url, json.dumps(path_data), headers=headers, verify=False)
            resp_json = resp.json()
            flowAnalysisId = resp_json["response"]["flowAnalysisId"]
            #print("flowAnalysisId: " + flowAnalysisId)
            check_url = api_url+"/"+flowAnalysisId
            #print("checkURL: " + check_url)
            resp = requests.get(check_url, headers=headers, verify=False)
            resp_json = resp.json()
            status = resp_json["response"]["request"]["status"]
            while status != "COMPLETED":
                print(color.GREEN+"Tracing..."+color.END)
                resp = requests.get(check_url, headers=headers, verify=False)
                resp_json = resp.json()
                status = resp_json["response"]["request"]["status"]
                if status == "FAILED":
                    break
            print(color.GREEN+"Status: " + status+color.END)

            #DISPLAY RESULTS OF PATH TRACE
            if status == "COMPLETED":
                path_source = resp_json["response"]["request"]["sourceIP"]
                path_dest = resp_json["response"]["request"]["destIP"]
                print(color.BOLD+"Source IP Address: " + path_source+color.END)
                print(color.BOLD+"Destination IP Address: " + path_dest+color.END)
                networkElementsInfo = resp_json["response"]["networkElementsInfo"]
                networkElementsInfo_list = []
                i = 0
                for item in networkElementsInfo:
                    i+=1
                    if ("id" in item):
                        itemId = item['id']
                    else:
                        itemId = "UNKNOWN"
                    if ("type" in item):
                        itemType = item['type']
                    else:
                        itemType = "UNKNOWN"
                    if ("ip" in item):
                        itemIP = item['ip']
                    else:
                        itemIP = "UNKNOWN"
                    if ("linkInformationSource" in item):
                        itemLIS = item['linkInformationSource']
                    else:
                        itemLIS = "UNKNOWN"
                    if ("ingressInterface" in item and "physicalInterface" in item["ingressInterface"] and "name" in item["ingressInterface"]["physicalInterface"]):
                        itemName = item["ingressInterface"]["physicalInterface"]["name"]
                    else:
                        itemName = "UNKNOWN"
                    networkElementsInfo1 = [i, itemId, itemType, itemIP, itemLIS, itemName]
                    networkElementsInfo_list.append( networkElementsInfo1 )
                table_header = ["Number", "ID", "Type", "IP", "Link-Information-Source", "Interface"]
                print(color.BOLD+"PATHTRACE:"+color.END)
                print(color.BOLD+ tabulate(networkElementsInfo_list, table_header, tablefmt="fancy_grid") +color.END)
            #pathTrace()
        else:
            print(printError)
            pathTrace()

    pathTrace()
