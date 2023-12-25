# Make python3 as default python instead of python2
sudo update-alternatives --install $(which python) python $(readlink -f $(which python3)) 3

# Install OpenCV
sudo apt-get install libcblas-dev -y
sudo apt-get install libhdf5-dev -y
sudo apt-get install libhdf5-serial-dev -y
sudo apt-get install libatlas-base-dev -y
sudo apt-get install libjasper-dev -y
sudo apt-get install libqtgui4 -y
sudo apt-get install libqt4-test -y
pip3 install opencv-python
pip3 install -U numpy

# Install Required Libraries
pip3 install -r requirements.txt