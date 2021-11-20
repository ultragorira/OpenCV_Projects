import cv2
import mediapipe as mp
import time


cap  = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDrawLines = mp.solutions.drawing_utils

prev_Time = 0
current_Time = 0

while True:

    success, img = cap.read()
    #Converting image to RGB
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmark.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id ==8:
                    cv2.circle(img, (cx, cy), 20, (0, 0, 255), cv2.FILLED) 
            
            mpDrawLines.draw_landmarks(img, hand_landmark, mpHands.HAND_CONNECTIONS)

    current_Time = time.time()
    fps = 1/(current_Time-prev_Time)
    prev_Time = current_Time

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (0, 0, 255), 2)

    cv2.imshow('image', img)
    cv2.waitKey(1)