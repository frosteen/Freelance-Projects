import time, serial

SERIAL_PORT = "/dev/ttyS0"    # Rasp 3 UART Port

ser = serial.Serial(SERIAL_PORT, baudrate=115200, timeout=10)
print("works")
ser.write("AT+CMGF=1\r".encode()) # set to text mode
time.sleep(1)
ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all SMS
time.sleep(1)
reply = ser.read(ser.inWaiting()).decode() # Clean buf
print("Listening for incomming SMS...")
while True:
    reply = ser.read(ser.inWaiting()).decode()
    if reply != "":
        ser.write("AT+CMGR=1\r".encode()) 
        time.sleep(0.5)
        reply = ser.read(ser.inWaiting()).decode("utf-8").strip()
        print(reply)
        print("SMS received. Content:")
        if "HI" in reply.upper():
            print("RECEIVED!")
            break
        time.sleep(0.5)
        ser.write('AT+CMGDA="DEL ALL"\r'.encode()) # delete all
        time.sleep(0.5)
        ser.read(ser.inWaiting()) # Clear buffer
        time.sleep(0.5)
    time.sleep(0.5)

