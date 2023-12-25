# Make python3 as default python instead of python2
sudo update-alternatives --install $(which python) python $(readlink -f $(which python3)) 3

# Install torch & torchvision
sudo apt install libopenblas-dev libblas-dev m4 cmake cython python3-dev python3-yaml python3-setuptools -y
export NO_CUDA=1
export NO_DISTRIBUTED=1
export NO_MKLDNN=1 
export BUILD_TEST=0
export MAX_JOBS=4
pip3 install https://github.com/Kashu7100/pytorch-armv7l/raw/main/torch-1.7.0a0-cp37-cp37m-linux_armv7l.whl
pip3 install https://github.com/Kashu7100/pytorch-armv7l/raw/main/torchvision-0.8.0a0%2B45f960c-cp37-cp37m-linux_armv7l.whl

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

# Install YOLOv5 Requirements
pip3 install -r requirements.txt