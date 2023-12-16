import json
import requests
json_data = json.loads(open("codebeautify.json").read())
#json_data = requests.get(open("codebeautify.json")).json()
print(json_data)
