import RPi.GPIO as GPIO
import time

try:
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(20,GPIO.IN)
except:
  GPIO.cleanup()
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(20,GPIO.IN)

while 1:
    read = GPIO.input(20)
    print(read)
