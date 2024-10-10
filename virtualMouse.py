import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui
wCam=640
hCam=480
frameR = 100
smooth = 5
plocX, plocY = 0,0
clocX, clocY = 0,0
cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 500)
pTime = 0

detector = htm.handDetector(maxHands=1)
width, height = pyautogui.size()
while True:
    success, img= cap.read()
    img = detector.findHands(img)
    lmlist, bbox=detector.findPosition(img)
    if len(lmlist)!=0:
        x1, y1=lmlist[8][1:]
        x2, y2=lmlist[12][1:]
        fingers=detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
        if fingers[1]==1 and fingers[0]==0:
            
            x3 = np.interp(x1, (frameR,wCam-frameR),(0,width))
            y3 = np.interp(y1, (frameR,hCam-frameR),(0,height))
            clocX = plocX + (x3-plocX)/smooth
            clocY = plocY + (y3-plocY)/smooth
            print(x3,y3)
            pyautogui.moveTo(width-clocX, clocY)
            cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        if fingers[1]==1 and fingers[0]==1:
            length, img, info=detector.findDistance(4,8,img)
            print(length)
            if length < 30:
                cv2.circle(img,(info[4],info[5]),15,(0,255,0),cv2.FILLED)
                pyautogui.click()


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)