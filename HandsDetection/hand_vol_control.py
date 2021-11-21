import cv2
import numpy as np
import mediapipe as mp
import time
import handDetector as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


width_camera, height_camera = 640, 480
cap  = cv2.VideoCapture(0)
cap.set(3, width_camera)
cap.set(4, height_camera)
prev_Time = 0
detector = htm.handDetector(detection_conf=0.8)

#Getting volume of device
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume_range = volume.GetVolumeRange()
min_volume = volume_range[0]
max_volume = volume_range[1]
volume_to_set = 0
volume_bar = 400
volume_perc = 0

while True:

    success, img = cap.read()
    img = detector.detect_hand(img)
    landmark_list = detector.findPos(img, draw = False) 

    if len(landmark_list) > 0:
        #Tip of thumnb is 4, Tip of index is 8
        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[8][1], landmark_list[8][2]
        #Center of the line
        cx, cy = (x1+x2)//2, (y1+y2)//2 
        cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)

        #convert range of length of line to range of volume

        volume_to_set = np.interp(length,[40,200], [min_volume, max_volume])
        volume.SetMasterVolumeLevel(volume_to_set, None)
        volume_bar = np.interp(length,[40,200], [400, 150])
        volume_perc = np.interp(length,[40,200], [0, 100])

        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 200, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (80, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volume_bar)), (80, 400), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, f'{int(volume_perc)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)

    current_Time = time.time()
    fps = 1/(current_Time-prev_Time)
    prev_Time = current_Time

    #cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (0, 0,255), 2)
    cv2.imshow('img', img)
    cv2.waitKey(1)