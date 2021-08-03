# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 20:16:37 2021

@author: Mahfuz_Shazol
"""


import cv2
import mediapipe as mp
import time
import math


class poseDetector():
        def __init__(self,static_image_mode=False,model_complexity=1,smooth_landmarks=True,min_detection_confidence=0.5,min_tracking_confidence=0.5):
              self.static_image_mode=static_image_mode
              self.model_complexity=model_complexity
              self.smooth_landmarks=smooth_landmarks
              self.min_detection_confidence=min_detection_confidence
              self.min_tracking_confidence=min_tracking_confidence
              
              self.mpDrow=mp.solutions.drawing_utils
              self.mpPose=mp.solutions.pose
              self.pose=self.mpPose.Pose(self.static_image_mode,
                                    self.model_complexity,
                                    self.smooth_landmarks,
                                    self.min_detection_confidence,
                                    self.min_tracking_confidence)

        def findPose(self,img,drow=True):
                  imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                  self.results=self.pose.process(imgRGB)
                  #print(results.pose_landmarks)
          
                  if self.results.pose_landmarks:
                      if drow:
                         self.mpDrow.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
                      
                  return img   
              
        def getPosition(self,img,drow=True):
                  self.lmkList=[]
                  if self.results.pose_landmarks:  
                       for id,lm in enumerate(self.results.pose_landmarks.landmark):
                            h,w,c=img.shape
                          
                            cx,cy=int(lm.x*w),int(lm.y*h)
                            self.lmkList.append([id,cx,cy])
                            if drow:
                               cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED) 
                               
                  return self.lmkList
      
        def findAngle(self,img,p1,p2,p3,draw=True):
            
               
                x1,y1=self.lmkList[p1][1:]
                x2,y2=self.lmkList[p2][1:]
                x3,y3=self.lmkList[p3][1:]
           
                angle=math.degrees(math.atan2(y3-y2, x3-x2)-math.atan2(y1-y2, x1-x2))
             
                if angle<0:
                   angle+=360
                if draw:
                    cv2.line(img, (x1,y1), (x2,y2), (255,255,255),3)
                    cv2.line(img, (x2,y2), (x3,y3), (255,255,255),3)
                    
                    cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
                    cv2.circle(img,(x1,y1),15,(255,0,0),2)
                    cv2.circle(img,(x2,y2),10,(255,0,0),cv2.FILLED)
                    cv2.circle(img,(x2,y2),15,(255,0,0),2)
                    cv2.circle(img,(x3,y3),10,(255,0,0),cv2.FILLED)
                    cv2.circle(img,(x3,y3),15,(255,0,0),2)
           
                    #cv2.putText(img,str(int(angle)),(x2-50,y2+50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
                    
                return angle    
    
def main():
    cTime=0
    pTime=0
    #cap=cv2.VideoCapture('2.mp4')
    cap=cv2.VideoCapture(0)
    detector=poseDetector()
    
    while True:
          success,img=cap.read()    
          cTime=time.time()
          fps=1/(cTime-pTime)
          pTime=cTime
          
          img=detector.findPose(img)
          lmkList=detector.getPosition(img)
          #print(lmkList)
          cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
          cv2.imshow("Images",img)
          cv2.waitKey(1)
          
          if cv2.waitKey(1) & 0xff==ord('c'):
              cap.release()
              cv2.destroyAllWindows()
              break;
    
    


          
          
if __name__=='__main__':
     main()          
