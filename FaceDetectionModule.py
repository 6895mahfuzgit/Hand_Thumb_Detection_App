# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 01:54:21 2021

@author: Mahfuz_Shazol
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 01:07:16 2021

@author: Mahfuz_Shazol
"""
import cv2
import mediapipe as mp
import time



class FaceDetector():
       def __init__(self,minDetectionCon=0.5):
              self.minDetection=minDetectionCon;
           
              self.mpFaceDetection=mp.solutions.face_detection
              self.mpDrow=mp.solutions.drawing_utils
              self.faceDetectio=self.mpFaceDetection.FaceDetection(self.minDetection)
              
       def findFaces(self,img,draw=True):
              imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
              self.results=self.faceDetectio.process(imgRGB)
              bboxs=[]
              if self.results.detections:
                   for id,detection in enumerate(self.results.detections):
                        #mpDrow.draw_detection(img,detection)
                        #print(id,detection)
                        #print(detection.score)
                        #print(detection.location_data.relative_bounding_box)
                        bboxC=detection.location_data.relative_bounding_box
                        ih,iw,ic=img.shape
                        bbox=int(bboxC.xmin*iw),int(bboxC.ymin*ih),\
                             int(bboxC.width*iw),int(bboxC.height*ih)
                             
                        bboxs.append([id,bbox,detection.score])     
                        if draw:
                            self.fancyDraw(img,bbox)
                            #cv2.rectangle(img, bbox,(255,0,1),1)  
                            cv2.putText(img,f'{int(detection.score[0]*100)}%',(bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2)      
              return img, bboxs 
        
       def fancyDraw(self,img,bbox,l=30,t=5,rt=1):
                x,y,w,h=bbox
                x1=x+w
                y1=y+h
                
                cv2.rectangle(img, bbox,(255,0,255),rt)  
                
                #top left x,y
                cv2.line(img,(x,y),(x+l,y),(255,0,255),t)
                cv2.line(img,(x,y),(x,y+l),(255,0,255),t)
                
                #top left x1,y
                cv2.line(img,(x1,y),(x1-l,y),(255,0,255),t)
                cv2.line(img,(x1,y),(x1,y+l),(255,0,255),t)
                
                #bottom right
                cv2.line(img,(x1,y1),(x1-l,y1),(255,0,255),t)
                cv2.line(img,(x1,y1),(x1,y1-l),(255,0,255),t)
                
                
                #bottom x,y1
                cv2.line(img,(x,y1),(x+l,y1),(255,0,255),t)
                cv2.line(img,(x,y1),(x,y1-l),(255,0,255),t)
                
                return img

def main():
    cTime=0
    pTime=0
    cap=cv2.VideoCapture(0)
    detector=FaceDetector()
    while True:
      success,img=cap.read()
      img,bboxs=detector.findFaces(img)
      
      print(bboxs)
      
      cTime=time.time()
      fps=1/(cTime-pTime)
      pTime=cTime
      
      
      cv2.putText(img,f'FPS:{int(fps)}',(70,50),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)      
      cv2.imshow("Images",img)
      cv2.waitKey(1)
      
      if cv2.waitKey(1) & 0xff==ord('c'):
             cap.release()
             cv2.destroyAllWindows()
             break;
         
             
if __name__=='__main__':
     main()          
             

