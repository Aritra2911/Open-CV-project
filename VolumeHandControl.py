import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


pTime = 0
cTime = 0

cap=cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
      IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol=0
volBar=150
volPer=100
while True:
   
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img,draw=False)
        if len(lmlist) != 0:
            #print(lmlist[4],lmlist[8])
            x1,y1= lmlist[4][1], lmlist[4][2]
            x2,y2= lmlist[8][1], lmlist[8][2]
            cx,cy = (x1+x2)//2, (y1+y2)//2
            cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
            cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
        
            length = math.hypot(x2-x1,y2-y1)
            #print(length)
            vol = np.interp(length,[5,160],[minVol, maxVol])
            volBar = np.interp(length,[20,160],[400,150])
            volPer = np.interp(length,[10,160],[0,100])
            print(vol)
            volume.SetMasterVolumeLevel(vol, None)

        cv2.rectangle(img, (50,150),(85,400),(255,0,255),3)
        cv2.rectangle(img, (50,int(volBar)),(85,400),(255,0,255),cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%',(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img,  str(int(fps)),(40,450),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)