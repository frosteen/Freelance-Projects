import serial, time
# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=10)

NUMBER = "09476207065"
MESSAGE = "HELLO WORLD!"

# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

port.write('AT\r\n'.encode())
time.sleep(1)
rcv = port.read(port.inWaiting()).decode("utf-8").strip()
print(rcv)

port.write('AT+CMGF=1\r\n'.encode())  # Select Message format as Text mode
time.sleep(1)
rcv = port.read(port.inWaiting()).decode("utf-8").strip()
print(rcv)
print("DONE THIS")

# Sending a message to a particular Number
port.write(('AT+CMGS="'+number+'"\r\n').encode())
time.sleep(2)
rcv = port.read(port.inWaiting()).decode("utf-8").strip()
print(rcv)

port.write((MESSAGE+'\r\n').encode())  # Message
time.sleep(1)
rcv = port.read(port.inWaiting()).decode("utf-8").strip()
print(rcv)

port.write("\x1A\r\n".encode()) # Enable to send SMS
time.sleep(1)
for i in range(10):
    rcv = port.read(port.inWaiting()).decode("utf-8").strip()
    print(rcv)
