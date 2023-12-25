import pyrebase
from datetime import datetime
import time

config = {
    "apiKey": "AIzaSyBz6KVh7zrUWtXKXh9RtR-mLBU5EPIv0qY",
    "authDomain": "guide-blind-people.firebaseapp.com",
    "databaseURL": "https://guide-blind-people-default-rtdb.firebaseio.com",
    "storageBucket": "guide-blind-people.appspot.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# while True:
#     dist = db.child("distance").get().val()
#     dt_string = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
#     print(f" {dt_string}  |   Object in {dist} cm.")
#     time.sleep(3)

def stream_handler(message):
    dist = message["data"]
    dt_string = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
    print(f" {dt_string} | Object in {dist} cm.")

my_stream = db.child("distance").stream(stream_handler)
