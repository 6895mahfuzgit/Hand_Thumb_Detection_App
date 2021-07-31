import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm 

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
while True:
      success, img = cap.read()
      img = detector.findHands(img)
      lmrList=detector.findPosition(img)
           
      if len(lmrList)!=0:
           if lmrList[4] :
               print(lmrList[4])
              
      cTime = time.time()
      fps = 1/(cTime-pTime)
      pTime = cTime
      cv2.putText(img, str(int(fps)), (10, 70),
                       cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
      cv2.imshow("Image", img)
      cv2.waitKey(1)
           
      if cv2.waitKey(1) & 0xff==ord('o'):
          cap.release()
          cv2.destroyAllWindows()
          break;