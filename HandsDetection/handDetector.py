import cv2
import mediapipe as mp
import time



class handDetector():
    def __init__(self, mode=False,maxHands=2, model_complexity=1,detection_conf=0.5, tracking_conf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = model_complexity
        self.detection_conf = detection_conf
        self.tracking_conf = tracking_conf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detection_conf, self.tracking_conf)
        self.mpDrawLines = mp.solutions.drawing_utils


    def detect_hand(self, img, draw = True):

        #Converting image to RGB
        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
           for hand_landmark in self.results.multi_hand_landmarks:
               if draw:               
                  self.mpDrawLines.draw_landmarks(img, hand_landmark, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPos(self, img, hand_number=0, draw = True):
            
        lm_list = []
        if self.results.multi_hand_landmarks:
            hand_to_detect = self.results.multi_hand_landmarks[hand_number]
            for id, lm in enumerate(hand_to_detect.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED) 
        return lm_list

def main():

    prev_Time = 0
    current_Time = 0
    cap  = cv2.VideoCapture(0)

    detector = handDetector()
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

if __name__ == '__main__':
    main()