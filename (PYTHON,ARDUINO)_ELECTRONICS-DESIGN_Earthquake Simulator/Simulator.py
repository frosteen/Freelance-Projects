import serial
from datetime import datetime
import time

# Settings
log_filename = "Logs/event_1637210817717_Thu_Nov_18_12_46_57_2021_05.log"
com_port = "COM5"


# Epoch Converter
def epoch_converter(epoch_time):
    return datetime.fromtimestamp(int(epoch_time) / 1000)


# Log Sender
def send_logs(log_file, ser):
    log_file = open(log_file, "r")
    read_logs = log_file.readlines()
    prev_seconds = 0
    for line in read_logs:
        line = line.strip()
        # lines with underscore are not sent to arduino
        _index, epoch_time, _x, _y, _z, intensity = line.split(",")
        # convert epoch time to %Y-%m-%d %H:%M:%S
        timestamp = epoch_converter(epoch_time).strftime("%Y-%m-%d %H:%M:%S.%f")
        # get epoch seconds
        seconds = float(str(int(epoch_time) / 1000)[8::])
        print(f"{_index}, {timestamp}, {_x}, {_y}, {_z}, {intensity}")
        # send intensity to arduino
        # print(intensity)
        ser.write(intensity.encode())
        # send data like in the logs
        time.sleep(seconds - prev_seconds)
        # get previous seconds
        prev_seconds = seconds
    log_file.close()


if __name__ == "__main__":
    try:
        # Initiate serial port
        ser = serial.Serial(port=com_port, baudrate=9600)
        input("Press ENTER to Start.")
        # Intiate sending logs to arduino
        send_logs(log_filename, ser)
    except Exception as e:
        print(f"!Error: {e}")
    finally:
        ser.close()
