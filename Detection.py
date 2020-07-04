#importing all required libraries
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import sys
import os

#initializing camera module, resolution, framerate and raw capture size
cam = PiCamera()
cam.framerate = 30
cam.resolution = (640, 480)
capture = PiRGBArray(cam, size = (640, 480))

#using Haar cascade model for frontal object detection
front_face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#creating the directories to store trusted faces
name = input("Your Name:")
dirct_name = "./face_img/" + name
print(dirct_name)
if not os.path.exists(dirct_name):
	os.makedirs(dirct_name)
print("Directory Created")

#taking video from pi camera as input and 30 frames as a platform to detect face in RGB mode
count = 1
for frame in cam.capture_continuous(capture, format="bgr", use_video_port=True):
        #storing the 30 gray scale images in the image directory of the person
		if count > 30:
				break
		frame = frame.array
		gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = front_face_cascade.detectMultiScale(gray_scale, scaleFactor = 1.5, minNeighbors = 5)
        #after converting it to gray scale it will only display a square around the face
		for (x, y, w, h) in faces:
				RGray = gray_scale[y:y+h, x:x+w]
				fname = dirct_name + "/" + name + str(count) + ".jpg"
				cv2.imwrite(fname, RGray)
				cv2.imshow("face", RGray)
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
				count += 1
				
				
		cv2.imshow('frame', frame)
		key = cv2.waitKey(1)
		capture.truncate(0)
		
		if key == 27:
			break

cv2.destroyAllWindows()
