import cv2 as cv
import time
import mediapipe as mp


class handDector():
    def __init__(self, static_image_mode=False,
                 max_num_hands = 2,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5
                 ):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        
        self.mpHands = mp.solutions.hands
        self.hand = self.mpHands.Hands(self.static_image_mode, 
                                       self.max_num_hands,
                                       self.min_detection_confidence,
                                       self.min_tracking_confidence
                                       )
        self.mpDraw = mp.solutions.drawing_utils
               
        
    def findHands(self, img, draw = True):
        image_RGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        image_FLIP = cv.flip(img, flipCode=1)
        img = cv.flip(image_RGB, flipCode=1)
        
        result = self.hand.process(img)
        self.detect_hand = result.multi_hand_landmarks
        if self.detect_hand:
            # print("hand is detected")
            for hands in self.detect_hand:
                if draw:
                    self.mpDraw.draw_landmarks(image_FLIP, hands, self.mpHands.HAND_CONNECTIONS)
        return image_FLIP
    
    
    def findPosition(self, img, handNo=0, draw = True):
        lmList = []
        
        
        if self.detect_hand:
            myHand = self.detect_hand[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(f"id : {id}")
                # print(f"lm : {lm}") #landmark in x,y,z
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                #print(id, cx, cy)
                # if int(id) == 0:
                # cv.putText(img, "t", (cx, cy), fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=10, color=(255, 255, 255), thickness=10)
                # print("id printing")
                if draw:
                    cv.circle(img, center=(cx, cy), radius=3, color=(255, 0, 255), thickness=6, lineType=cv.FILLED)
        
            return lmList
      



def main():    
    camera = cv.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = handDector()
    
    if not camera.isOpened():
        print("camera is not opened")
        exit()
    
    while True:
        frame, img = camera.read()  # read returns a tuple(boolean, img(numpy))
        image_FLIP = detector.findHands(img)
        
        fingures = detector.findPosition(image_FLIP)
        if fingures != None:        
            print(fingures)
                                                    
        # frame per second
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(image_FLIP, str(int(fps)), (50, 100), cv.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 255, 255), thickness=5)
        
        cv.imshow('image', image_FLIP)
        # cv.imshow('image', image_RGB)
        
        if cv.waitKey(1) == ord('q'):
            break
    
    camera.release()
    cv.destroyAllWindows()



if __name__ == "__main__":
    main();