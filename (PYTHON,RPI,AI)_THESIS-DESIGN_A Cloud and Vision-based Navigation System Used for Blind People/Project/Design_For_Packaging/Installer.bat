@echo off
call python-3.7.9-amd64.exe
pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
pip install pyrebase4
pip install imutils
pip install num2words
pip install opencv-python
pip install numpy
pip install torch torchvision torchaudio
md c:\PC_GUI
md c:\PC_GUI\PyQt5_Dependencies
md c:\PC_GUI\Capture
copy Files\* c:\PC_GUI
copy Files\PyQt5_Dependencies\* c:\PC_GUI\PyQt5_Dependencies
copy Files\PC_GUI.bat "%USERPROFILE%\Desktop"
::pause