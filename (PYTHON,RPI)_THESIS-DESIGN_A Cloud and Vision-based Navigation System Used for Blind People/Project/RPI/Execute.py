import os
import time

time.sleep(10)

os.system(
    "gst-launch-1.0 -v v4l2src device=/dev/video0 num-buffers=-1 ! video/x-raw,width=640,height=480, framerate=30/1 ! videoconvert ! jpegenc ! tcpserversink  host=localhost port=5000 &"
)
os.system("cd /home/pi/Desktop && python3 RPI.py &")
