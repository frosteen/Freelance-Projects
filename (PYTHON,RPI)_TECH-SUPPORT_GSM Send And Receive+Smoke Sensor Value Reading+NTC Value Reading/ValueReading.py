import Adafruit_ADS1x15, time

_gain = 1
adc = Adafruit_ADS1x15.ADS1115()
while 1:
    smokeSensorVal = adc.read_adc(0, gain=_gain)
    NTCVal = adc.read_adc(1, gain=_gain)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("SmokeSensorValue:", smokeSensorVal)
    print("NTC Value:",NTCVal)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    time.sleep(1)
