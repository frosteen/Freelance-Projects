cd /home/pi/Flir/flirone-v4l2_luporl && sh load_module.sh
sudo ./flirone palettes/Iron2.raw -v 2 &
cd /home/pi/Program/ && python MainWindow.py
