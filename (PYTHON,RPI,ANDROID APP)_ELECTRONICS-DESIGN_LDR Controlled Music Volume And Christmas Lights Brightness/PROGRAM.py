import os
from threading import Thread
import alsaaudio
from gpiozero import LightSensor
from gpiozero import LED
from time import sleep
import random
directory = "/home/pi/Desktop/"
m = alsaaudio.Mixer()
current_volume = m.getvolume() # Get the current Volume
m.setvolume(100) # Set the volume to 70%.

def ThreadMusic():
    try:
        os.system("killall -9 mpg123")
    except: pass
    os.system("mpg123 -q --loop -1 "+directory+"Song.mp3 &")
th = Thread(target=ThreadMusic)
th.daemon = True
th.start()

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
speed = 0.1
leds = [LED(17),LED(27),LED(22),LED(5),LED(6),LED(13),LED(19),LED(26)]
def ThreadLights():
    global speed
    while True:
        try:
            n = random.randrange(0,8,1)
            m = random.randrange(0,8,1)
            while n == m:
                m = random.randrange(0,8,1)
            leds[n].on()
            leds[m].on()
            sleep(speed)
            leds[n].off()
            leds[m].off()
            sleep(speed)
        except: pass
th1 = Thread(target=ThreadLights)
th1.daemon = True
th1.start()

ldr = LightSensor(4)
while True:
    newValue = translate(ldr.value,0,0.8,100,20)
    speed = translate(ldr.value,0,0.8,0.05,1.5)
    print(speed)
    if speed < 0:
        speed = 0.05
    if newValue < 0:
        newValue = 0
    if newValue > 100:
        newValue = 100
    m.setvolume(round(newValue))

