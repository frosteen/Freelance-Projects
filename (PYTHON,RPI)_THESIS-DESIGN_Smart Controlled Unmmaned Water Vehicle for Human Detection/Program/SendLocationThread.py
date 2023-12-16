import time
from threading import Thread

import serial

from AdvanceSendEmail import send_email
from MySIM800L import MySIM800L
from ParseGPS import parse_gps
from ReadWriteCSV import write_csv_dict
import time
import datetime


class SendLocation:
    def __init__(
        self,
        port_GPS="/dev/ttyS0",
        port_SIM800L="/dev/ttyUSB0",
        cellphone_number="+639476207065",
        email_username="unmanned.vehicle.2022@gmail.com",
        email_password="unmannedvehicle@2022",
        name="SendLocation",
    ):
        self.name = name
        self.is_checking = False
        self.serial_GPS = serial.Serial(port=port_GPS, baudrate=9600)

        # try ttyUSB0 else ttyUSB1
        try:
            self.SIM800L = MySIM800L(port_SIM800L)
        except Exception as e:
            self.SIM800L = MySIM800L("/dev/ttyUSB1")

        self.cellphone_number = cellphone_number
        self.email_username = email_username
        self.email_password = email_password

    def parsed_gps_data(self):
        decoded_data = self.serial_GPS.readline().decode()
        parsed_gps_data = parse_gps(decoded_data)
        return parsed_gps_data

    def wait_to_initialize(self):
        while 1:
            try:
                print("Initializing GPS...")
                parsed_gps_data = self.parsed_gps_data()
                if parsed_gps_data is not None:
                    if not None in parsed_gps_data:
                        print("GPS Okay!")
                        break
            except Exception as e:
                pass

    def start(self, file_path, num_people):
        if not self.is_checking:  # if not checking then start thread
            t = Thread(target=self.update, name=self.name, args=[file_path, num_people])
            t.daemon = True
            t.start()
        return self

    def csv_log(self, date, name, processing_time):
        write_csv_dict(
            "Logs.csv",
            {
                "Date": date,
                "Name": name,
                "Processing Time": processing_time,
            },
        )

    def update(self, file_path, num_people):
        self.is_checking = True
        while 1:
            try:
                parsed_gps_data = self.parsed_gps_data()
                if parsed_gps_data is not None:
                    if not None in parsed_gps_data:
                        # parse data
                        (
                            timestamp,
                            latitude,
                            longitude,
                            altitude,
                            altitude_units,
                        ) = parsed_gps_data

                        # adjust timestamp to GMT+8
                        timestamp = str(timestamp).split(":")
                        hours = (
                            int(timestamp[0]) + 8
                            if int(timestamp[0]) + 8 < 24
                            else int(timestamp[0]) - 16
                        )
                        minutes, seconds = timestamp[1:]

                        # create output
                        output = f"The Ship detected {num_people} people!\n\n"
                        output += f"Timestamp: {hours}:{minutes}:{seconds}\n"
                        output += f"Altitude: {abs(altitude)} {altitude_units}\n"
                        output += f"https://maps.google.com/?q={latitude},{longitude}"
                        print(output)

                        # send sms
                        sms_time_start = time.time()
                        self.SIM800L.send_sms(self.cellphone_number, output)
                        self.csv_log(
                            datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                            f"SMS Send Time",
                            time.time() - sms_time_start,
                        )

                        print("SMS sent!")

                        # email captured image
                        try:
                            email_time_start = time.time()
                            is_email_sent = send_email(
                                self.email_username,
                                self.email_password,
                                self.email_username,
                                "Ship Notification Email",
                                output,
                                file_path=file_path,
                            )
                            if is_email_sent:
                                print("Email sent!")
                            self.csv_log(
                                datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                                f"Email Send Time",
                                time.time() - email_time_start,
                            )
                        except Exception as e:
                            pass

                        self.is_checking = False
                        return

            except Exception as e:
                pass


if __name__ == "__main__":
    import time

    SendLocation = SendLocation()
    while 1:
        print("Test Send.")
        SendLocation.start("Captured/Captured.jpg")
        time.sleep(3)
