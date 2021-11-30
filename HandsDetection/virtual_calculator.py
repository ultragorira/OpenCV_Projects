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


def create_button(image, button_list):
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 55), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 4)
    return(image)
class Calculator_GUI():
    
    def __init__(self, pos, text, size=[60, 60]):
        self.pos = pos
        self.text = text
        self.size = size
        

for i, text in enumerate(list_buttons):
    for j, button in enumerate(list_buttons[i]):
        if not button == '':
            buttons_to_add.append(Calculator_GUI([100 * j + 50, 100 * i + 50], button))

while True:

    success, img = cap.read()
    img = detector.detect_hand(img)
    landmark_list = detector.findPos(img)
    img = create_button(img, buttons_to_add)
    #Calculator Output
    cv2.rectangle(img, (40, 450), (410,500), (255, 0, 0), cv2.FILLED)

    #Check if any landmark found
    if landmark_list:
        for button in buttons_to_add:
            x, y = button.pos
            w, h = button.size
            print(f'landmark x {landmark_list[8][1]} y {landmark_list[8][2]}')
            print(x)
            print(w)

            if x < landmark_list[8][1] < x+w and y < landmark_list[8][2] < y + h: 
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 10, y + 55), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 4)



    cv2.imshow('img', img)
    cv2.waitKey(1)