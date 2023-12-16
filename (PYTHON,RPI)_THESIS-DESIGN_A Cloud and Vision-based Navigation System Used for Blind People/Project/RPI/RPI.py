import subprocess
from threading import Thread

import pyttsx3
import RPi.GPIO as GPIO

import Firebase


def speak_text(command):
    engine = pyttsx3.init()  # Initialize the engine
    engine.setProperty("rate", 100)  # setting up new voice rate
    engine.setProperty("volume", 1.0)  # setting up volume level  between 0 and 1
    engine.say(command)
    engine.runAndWait()
    engine.stop()


def update_tcp_url():
    speak_text("Device is connecting. Please wait.")
    print("Updating TCP_URL...")
    cmd = "ngrok tcp 5000 --log=stdout"
    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
    while True:
        line_with_ngrok_url = p.stdout.readline().strip().decode("utf-8")
        if line_with_ngrok_url.find("started tunnel") != -1:
            url_only = line_with_ngrok_url[
                line_with_ngrok_url.index("url=") + len("url=") :
            ]
            Firebase.update("/", {"TCP_URL": url_only})
            break
    print("Updating TCP_URL... Done!")
    speak_text("Device successfully connected.")


def sentence_checker():
    while True:
        if Firebase.get("is_processing") == True:
            print("Image is being processed. You can now move.")
            speak_text("Image is processing.")
            Firebase.update("/", {"is_processing": False})
        elif Firebase.get("/Sentence") != "":
            sentence = Firebase.get("/Sentence")
            print(sentence)
            Firebase.update("/", {"Sentence": ""})
            speak_text(sentence)


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN)
    print("Start checking GPIO.BCM 23 press.")
    while True:
        if GPIO.input(23) == GPIO.HIGH:
            print("GPIO.BCM 23 pressed!")
            speak_text("Button pressed. Please wait.")
            Firebase.update("/", {"Execute": True})


if __name__ == "__main__":
    Thread(target=sentence_checker, daemon=True).start()
    update_tcp_url()
    main()
