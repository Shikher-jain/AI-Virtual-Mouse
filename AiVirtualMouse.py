'''
1) Find the hand landmarks
2) Find the tip of the middle and Index fingers
3) Find the fingers up or down
4) Only the index finger is up means Moving Mode
5) convet coordinats
6) smothing values
7) Move Mouse
8) Both Index and Middle fingers are up means Clicking Mode
9) Find the distance between the two fingers
10) Click mouse if dist. short
11) FPS
12) Display

'''

import handTrackingModule as htm
import numpy as np
import autopy
import time
import cv2

wCam, hCam = 640, 480
wScr, hScr = autopy.screen.size()  # Get screen size
# print(wScr, hScr)

frameR = 100  # Frame Reduction
smoothening = 7

xp, yp = 0, 0
xc, yc = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)


pTime = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]    # Index finger tip
        x2, y2 = lmList[12][1:]   # Middle finger tip

        fingers = detector.fingersUp()
        print(fingers)

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            
            # Convert coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # Smoothen values
            # x3 = int((x3 + (wScr - x3) / smoothening))
            # y3 = int((y3 + (hScr - y3) / smoothening))
            
            xc = int((xp + (x3-yp) / smoothening))
            yc = int((yp + (y3-yp) / smoothening))
            
            # Move mouse
            autopy.mouse.move(x3, y3)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED) 
            xp, yp = xc, yc

        if fingers[1] == 1 and fingers[2] == 1:
            # Clicking Mode
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)

            # Click mouse if distance is short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED) 
                autopy.mouse.click()



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img,f"FPS:{int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

