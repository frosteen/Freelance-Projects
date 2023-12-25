import time

import serial


class MySIM800L:
    def __init__(self, port="/dev/ttyS0"):
        self.serial = serial.Serial(port, baudrate=9600)

    def command(self, command):
        self.serial.write(command)
        time.sleep(0.2)
        return self.serial.readline().decode().strip()

    def send_sms(self, cellphone_number, message):
        self.command("AT\r".encode())  # initialize
        self.command("AT+CMGF=1\r".encode())  # text mode
        self.command(('AT+CMGS="' + cellphone_number + '"\r').encode())
        self.command((message + "\r").encode())  # write message
        self.command("\x1A\r".encode())  # execute

    def get_incoming_sms(self):
        self.command("AT\r".encode())  # initialize
        self.command("AT+CMGF=1\r".encode())  # text mode
        self.command('AT+CMGDA="DEL ALL"\r'.encode())  # delete all sms
        while 1:
            message = self.serial.readline().decode().strip()
            if message != "":
                self.command("AT+CMGR=1\r".encode())  # receive mode
                self.command('AT+CMGDA="DEL ALL"\r'.encode())  # delete all sms
                return message


if __name__ == "__main__":
    SIM800L = MySIM800L("/dev/ttyUSB0")
    SIM800L.send_sms("+639476207065", "TESTING 1234")
