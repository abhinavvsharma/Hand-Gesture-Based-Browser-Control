# Hand-Gesture Based Browser Control
This repository contains the code-base for Hand-Gesture Based Browser Control, a Python program to control functions of a browser through hand-gestures.
# Setup

### Requires Python 3.x (tested with Python 3.8)
```
Clone this repository.
pip install -r Hand-Gesture-Based-Browser-Control/requirements.txt
```
Optional steps for using a conda environment before installing the requirements above:
```
conda create -n hciproject python==3.8
conda activate hciproject
```
# Data input formats
Hand-gestures are sued as input data for the system. For using other cameras than system's primary camera, change the digit on (Line 41) in the "main.py" i.e., "cap = cv2.VideoCapture(0)".

# Project Report
Project report can be found [here](https://github.com/abhinavvsharma/Hand-Gesture-Based-Browser-Control/blob/main/Report.pdf)

# Project Video
Project demonstration video can be found [here](https://drive.google.com/file/d/1Sq4qFwDnSoYrq9LJQKk2l2-Imz_3NJKz/view?usp=sharing).
