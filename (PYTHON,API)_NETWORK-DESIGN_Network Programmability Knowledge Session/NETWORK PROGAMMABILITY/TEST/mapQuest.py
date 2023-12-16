import urllib.parse
import requests

while True:
    main_api = "https://www.mapquestapi.com/directions/v2/route?"
    orig = input("ORIGIIN: ")
    if orig == "q":
        break
    dest = input("DEST: ")
    if dest == "q":
        break
    key = "3jLcI5tR0zYlF2jLnqGiNB8JSC8ZJWXe"
    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})

    json_data = requests.get(url).json()
    status_data = json_data["info"]["statuscode"]
    if status_data == 0:
        print("SUCCESS!")
    elif status_data == 402:
        print("Invalid Input")
        break
    locateManuever = json_data["route"]["legs"][0]["maneuvers"]
    for x in locateManuever:
        print("DISTANCE: " + str(x["distance"]))
        print("NARRATIIVE: " + x["narrative"])
        print("---------------------------------------")
