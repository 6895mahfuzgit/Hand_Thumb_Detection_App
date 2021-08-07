import cv2
import mediapipe as mp
import time
import math


class handDetector():
   def __init__(self, mode=False, maxHand=2, detectionConf=0.5, trackConf=0.5):
       self.mode = mode
       self.maxHand = maxHand
       self.detectionConf = detectionConf
       self.trackConf = trackConf

       self.mpHands = mp.solutions.hands
       self.hands = self.mpHands.Hands(
           self.mode, self.maxHand, self.detectionConf, self.trackConf)
       self.mpDraw = mp.solutions.drawing_utils
       
       self.tipIds=[4,8,12,16,20]
       self.lmkList=[]

   def findHands(self, img, draw=True):
       imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

       self.results = self.hands.process(imgRGB)
       #print(results.multi_hand_landmarks)
       if self.results.multi_hand_landmarks:
           for handLms in self.results.multi_hand_landmarks:
               if draw:
                   self.mpDraw.draw_landmarks(
                       img, handLms, self.mpHands.HAND_CONNECTIONS)
       return img

                


   def findPosition(self,img,handNo=0,draw=True):
       self.lmkList=[]
       if self.results.multi_hand_landmarks:
           handLms=self.results.multi_hand_landmarks[handNo]
           for id,lm in enumerate(handLms.landmark):
                 h,w,c=img.shape
                 cx , cy =int(lm.x*w) , int(lm.y*h)
                 #print(id,cx,cy)
                 self.lmkList.append([id,cx,cy])
                 if draw:
                     cv2.circle(img,(cx,cy), 7, (255,0,0),cv2.FILLED)
       return self.lmkList      
   
    
   
   def findSumthPosition(self, img, handNo=0, draw=True):
            xList = []
            yList = []
            bbox = []
            self.lmkList = []
            if self.results.multi_hand_landmarks:
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    xList.append(cx)
                    yList.append(cy)
                    # print(id, cx, cy)
                    self.lmkList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            if len(xList)!=0:
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax
        
                if draw:
                    cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                    (0, 255, 0), 2)
        
            return self.lmkList, bbox
 
   
   def fingursUp(self):
            fingers=[]
            if self.lmkList[self.tipIds[0]][1]<self.lmkList[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            #4 fingers
            for id in range(1,5):    
                if self.lmkList[self.tipIds[id]][2]<self.lmkList[self.tipIds[id]-2][2]:
                   fingers.append(1) 
                else:
                   fingers.append(0)
                   
            return fingers   
   
   def findDistance(self, p1, p2, img, draw=True,r=15, t=3):
            x1, y1 = self.lmkList[p1][1:]
            x2, y2 = self.lmkList[p2][1:]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            
            if draw:
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
                cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)
            return length, img, [x1, y1, x2, y2, cx, cy]        
        

def main():
     pTime = 0
     cTime = 0
     cap = cv2.VideoCapture(0)
     detector = handDetector()
     while True:
           success, img = cap.read()
           img = detector.findHands(img)
           lmkList, bbox=detector.findSumthPosition(img)
           #lmrList=detector.findPosition(img)
           
           if len(lmkList)!=0:
               if lmkList[4] :
                  print(lmkList[4])
              
           cTime = time.time()
           fps = 1/(cTime-pTime)
           pTime = cTime
           cv2.putText(img, str(int(fps)), (10, 70),
                       cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
           cv2.imshow("Image", img)
           cv2.waitKey(1)
           
           if cv2.waitKey(1) & 0xff==ord('c'):
               cap.release()
               cv2.destroyAllWindows()
               break;

if __name__ == "__main__":
       main()
