# use python3 as default
sudo update-alternatives --install $(which python) python $(readlink -f $(which python3)) 3

# install required libraries for RPI.py
sudo apt install python3-pip
pip3 install pyttsx3
pip3 install firebase_admin
sudo apt-get update && sudo apt-get install espeak -y

# install required libraries for gstreamer
sudo apt-get install libx264-dev libjpeg-dev -y
sudo apt-get install libgstreamer1.0-dev \
     libgstreamer-plugins-base1.0-dev \
     libgstreamer-plugins-bad1.0-dev \
     gstreamer1.0-plugins-ugly \
     gstreamer1.0-tools -y
sudo apt-get install gstreamer1.0-gl gstreamer1.0-gtk3 -y