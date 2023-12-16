import RPi.GPIO as GPIO
import time
import num2words
import pyttsx3

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 

def speak_text(command):
    engine = pyttsx3.init()  # Initialize the engine
    engine.setProperty("rate", 110)  # setting up new voice rate
    engine.setProperty("volume", 1.0)  # setting up volume level  between 0 and 1
    engine.say(command)
    engine.runAndWait()
    engine.stop()



def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            dist = int(dist)
            print("Distance = %.1f cm" % dist)
            sentence = f"object in {num2words.num2words(dist)} cm"
            speak_text(sentence)
            time.sleep(3)
 
    except KeyboardInterrupt:
        print("stopped.")
        GPIO.cleanup()