# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 01:07:16 2021

@author: Mahfuz_Shazol
"""
import cv2
import mediapipe as mp
import time


cTime=0
pTime=0
cap=cv2.VideoCapture(0)

mpFaceDetection=mp.solutions.face_detection
mpDrow=mp.solutions.drawing_utils
faceDetectio=mpFaceDetection.FaceDetection(min_detection_confidence=0.8)

while True:
      success,img=cap.read()
      imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
      results=faceDetectio.process(imgRGB)
      if results.detections:
           for id,detection in enumerate(results.detections):
                #mpDrow.draw_detection(img,detection)
                #print(id,detection)
                #print(detection.score)
                #print(detection.location_data.relative_bounding_box)
                bboxC=detection.location_data.relative_bounding_box
                ih,iw,ic=img.shape
                bbox=int(bboxC.xmin*iw),int(bboxC.ymin*ih),\
                     int(bboxC.width*iw),int(bboxC.height*ih)
                cv2.rectangle(img, bbox,(0,0,255),1)  
                cv2.putText(img,f'{int(detection.score[0]*100)}%',(bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_PLAIN,3,(255,0,1),2)      
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

