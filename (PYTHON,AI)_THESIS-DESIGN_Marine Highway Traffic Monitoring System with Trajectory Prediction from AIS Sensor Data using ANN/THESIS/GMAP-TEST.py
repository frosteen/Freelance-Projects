import requests

url = "https://maps.googleapis.com/maps/api/staticmap?"

location = input("Enter location : ")

center = location

zoom = 10

api_key = "AIzaSyBjjB0_8bv-G6YfPft4IXFfwjSFlIbMu5U"

r = requests.get("https://maps.googleapis.com/maps/api/staticmap?center=%2214.58,120.962375%22&scale=4&zoom=12&size=1280x720&key=AIzaSyBjjB0_8bv-G6YfPft4IXFfwjSFlIbMu5U")

print(url + "center=" + center +"&zoom="+str(zoom)+"&size=1280x720&key="+api_key)

f = open('GMAP_IMAGE.png','wb')

f.write(r.content)

f.close()
