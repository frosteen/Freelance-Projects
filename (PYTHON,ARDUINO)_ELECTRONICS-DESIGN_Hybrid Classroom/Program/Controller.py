import serial
import keyboard
import time


def start_control(ser):
    is_control = False
    print("Toggle 'DOWN' Key to Activate Control")
    print("Press 'LEFT' or 'RIGHT' Key to ROTATE")
    while True:
        key = keyboard.read_key()
        if is_control:
            if key == "left":
                ser.write("A".encode())
            if key == "right":
                ser.write("B".encode())
        if key == "down":
            if is_control:
                is_control = False
                print("$ Control DEACTIVATED")
            else:
                is_control = True
                print("$ Control ACTIVATED")
            time.sleep(0.50)
        time.sleep(0.10)


def main():
    COMPORT = input("Input COMPORT:").upper()
    ser = serial.Serial(port=COMPORT, baudrate=9600)
    try:
        start_control(ser)
    except Exception as e:
        print(e)
    finally:
        print("Program stopped.")
        ser.close()


if __name__ == "__main__":
    main()
