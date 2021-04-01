import cv2 as cv
import time
import numpy as np
import tracking_module as tk
import math

###audio library
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#########window size
wcam, hcam = 680, 480
#############window size



camera = cv.VideoCapture(0)
camera.set(3, wcam)
camera.set(4, hcam)

cTime = 0
pTime = 0

detector = tk.handDector(min_detection_confidence = 0.7)
distance = 0

############checking camera is on or not
if not camera.isOpened():
    print("Your camera is not opened: ")
    exit()
##############end _ checking camera is on or not
    
    
####################audio control


#volume.GetMute()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
masterVol = volume.GetMasterVolumeLevel() # gices volume level 

print(masterVol)


#####setting the ranges
minvol = volRange[0]
maxvol = volRange[1]
################### end- audio control
    
########### start infinite loopp
vol = 400
volBar = 400
volPer = masterVol
while True:
    frame, image = camera.read()
    if not frame:
        print("camera is not capturing the images")
        exit()
    image = detector.findHands(image)
    fingures = detector.findPosition(image, draw=False)
    if fingures!=None:
        #print(fingures[3])
        x1, y1 = int(fingures[4][1]), int(fingures[4][2])
        x2, y2 = int(fingures[8][1]), int(fingures[8][2])
        cx, cy = (x1+x2)//2, (y1+y2)//2
            
        #first endpoint
        cv.circle(image, center=(x1, y1), radius=3, color=(255, 0, 255), thickness=6, lineType=cv.FILLED)
        #second endpoint
        cv.circle(image, center=(x2, y2), radius=3, color=(255, 0, 255), thickness=6, lineType=cv.FILLED)
        #line between two endpoints
        cv.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
        #point in the center of the line 
        cv.circle(image, center=(cx, cy), radius=3, color=(255, 0, 255), thickness=6, lineType=cv.FILLED)
        distance = math.hypot(x1-x2, y1-y2)
        #min = 10
        #max = 135
        
        #print(distance)
        if distance<12:
            #if distance is minimum then put a point         
            cv.circle(image, center=(cx, cy), radius=3, color=(0, 0, 0), thickness=6, lineType=cv.FILLED)
        
        if distance>=130:
            #if distance is minimum then put a point         
            cv.circle(image, center=(cx, cy), radius=3, color=(47, 47, 237), thickness=6, lineType=cv.FILLED)
        
        vol = np.interp(distance, [10, 130], [minvol, maxvol])
        volBar = np.interp(distance, [10, 130], [400, 200])
        volPer = np.interp(distance, [10, 130], [0, 100])
        #print(distance, vol)
        volume.SetMasterVolumeLevel(vol, None)  #sets the volume level min=-60, max = 0.0
        
     
    
          
    cv.rectangle(image, (30, 200), (60, 400), color=(0, 255 , 0), thickness=3)
    #cv.rectangle(image, (30, vol), (60, 400), color=(0, 255 , 0), thickness=5, lineType=cv.FILLED)
    cv.rectangle(img=image, pt1=(30, int(volBar)), pt2=(60, 400), color=(0, 255, 0), thickness=cv.FILLED)
    
    cv.putText(image, f"{int(volPer)}%", (20, 180), cv.FONT_HERSHEY_PLAIN, fontScale=3, color=(20, 200, 100), thickness=5)
    
    
            
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(image, str(int(fps)), (50, 100), cv.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 255, 255), thickness=5)
        
    cv.imshow("image", image)

    
    if cv.waitKey(1) == ord('q'):
        break
    
camera.release()
cv.destroyAllWindows()