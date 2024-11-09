import cv2
import mediapipe as mp
import time
import math



capture = cv2.VideoCapture(0) # opens webcam
mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 1,1,0.4,0.4)
mpDraw = mp.solutions.drawing_utils

moveForward = False
moveBackward = False
rotateLeft = False
rotateRight = False
stopAll = True
highFive = False

countUp= 0

middleDisplacement = 0

closenessMax = 0.9 
closenessMin = 0.5

leftDistanceMax = -80
rightDistanceMax = 80

while True: #instead of while loop, make sure this is part of arduino loop
    success, img = capture.read() # success means successfully read, img is numpy array representing image
    img = cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    imgHeight, imgWidth, imgChannel = img.shape
    middleLine = math.floor(imgWidth/2)

    if results.multi_hand_landmarks:
        for singleHand in results.multi_hand_landmarks:
            # mpDraw.draw_landmarks(img, singleHand)
            # calculating average position of palm
            ref1 = singleHand.landmark[5]
            ref2 = singleHand.landmark[9]
            ref3 = singleHand.landmark[13]
            ref4 = singleHand.landmark[17]
            ref5 = singleHand.landmark[0]

            avgX = int(((ref1.x + ref2.x + ref3.x + ref4.x + ref5.x)/5)*imgWidth)
            avgY = int(((ref1.y + ref2.y + ref3.y + ref4.y + ref5.y)/5)*imgHeight)

            middleDisplacement = int(middleLine - avgX)
            cv2.putText(img, str(middleDisplacement), (avgX,avgY), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 2)

            cv2.circle(img, (avgX,avgY), 5, (0,255,0), -1)
            cv2.line(img, (int(ref1.x * imgWidth), int(ref1.y * imgHeight)),(int(ref5.x * imgWidth), int(ref5.y * imgHeight)), (255, 0, 0), 2)

            refLineLength = round(math.sqrt(((ref1.x - ref5.x)**2) + ((ref1.y - ref5.y)**2)), 2)
            cv2.putText(img, str(refLineLength), (int(ref1.x * imgWidth), int(ref1.y * imgHeight)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 2)

            if middleDisplacement > rightDistanceMax: 
                rotateLeft = True
                rotateRight = moveForward = moveBackward = stopAll = highFive = False
                countUp = 0
            
            if middleDisplacement < leftDistanceMax: 
                rotateRight = True
                rotateLeft = moveForward = moveBackward = stopAll = highFive = False
                countUp = 0

            if middleDisplacement < rightDistanceMax & middleDisplacement > leftDistanceMax:
                rotateRight = False
                rotateLeft = False

                if refLineLength > closenessMax:
                    moveBackward = True
                    moveForward = stopAll = highFive = False
                    countUp = 0

                if refLineLength < closenessMin:
                    moveForward = True
                    moveBackward = stopAll = highFive = False
                    countUp = 0

                if refLineLength > closenessMin & refLineLength < closenessMax:
                    moveForward = moveBackward = rotateLeft = rotateRight = highFive = False
                    count = count + 1        
    
    

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to exit
        break


# if static_image_mode is true, it will always try to detect and track a subject, which is slow
# if false, it will only detect if the tracking confidence is below a certain range

