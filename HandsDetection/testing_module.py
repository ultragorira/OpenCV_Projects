import cv2
import mediapipe as mp
import time
import handDetector as htm

prev_Time = 0
current_Time = 0
cap  = cv2.VideoCapture(0)

detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.detect_hand(img)
    lm_list = detector.findPos(img)
    if len(lm_list) != 0:
       print(lm_list[8])
    current_Time = time.time()
    fps = 1/(current_Time-prev_Time)
    prev_Time = current_Time

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (0, 0, 255), 2)

    cv2.imshow('image', img)
    cv2.waitKey(1)