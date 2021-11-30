from typing import Text
import cv2
import numpy as np
import mediapipe as mp
from numpy.lib.polynomial import polysub
import handDetector as htm


width_camera, height_camera = 1288, 720
cap = cv2.VideoCapture(0)
cap.set(3, width_camera)
cap.set(4, height_camera)
detector = htm.handDetector(detection_conf=0.80)
buttons_to_add = []
list_buttons = [['7','8', '9', '/'], ['4', '5', '6', '*'], ['1', '2', '3', '-'], ['','0', '', '+']]

class Calculator_GUI():
    def __init__(self, pos, text, size=[60, 60]):
        self.pos = pos
        self.text = text
        self.size = size
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, self.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, self.text, (x + 13, y + 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 4)



while True:

    success, img = cap.read()
    img = detector.detect_hand(img)
    landmark_list = detector.findPos(img)

    for i, text in enumerate(list_buttons):
        for j, button in enumerate(list_buttons[i]):
            buttons_to_add.append(Calculator_GUI([100 * j + 50, 100 * i + 50], button))



    cv2.imshow('img', img)
    cv2.waitKey(1)