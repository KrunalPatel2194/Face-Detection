#importing all required libraries
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
import pickle

#setting up servo motor and assigning the pin
servo_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

#created PWM channel at 50Hz frequency
p = GPIO.PWM(servo_pin, 50)    
p.start(2.5)

with open('labels', 'rb') as f:
	dicti = pickle.load(f)
	f.close()

#initializing the camera setting resolution and frame rates and converting raw capture to PiRGBArray
cam = PiCamera()
cam.framerate = 30
cam.resolution = (640, 480)
capture = PiRGBArray(cam, size = (640, 480))

#using harcascade for face detection and LBPH recognizer for recognizing the faces and loading the trainer.yml file
front_face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
lbph_recognizer = cv2.face.createLBPHFaceRecognizer()
lbph_recognizer.load("train.yml")


#launch the Pi camera and starts recording video frames 
#convert the video frames in gray scale
for frame in cam.capture_continuous(capture, format="bgr", use_video_port=True):
	frame = frame.array
	gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = front_face_cascade.detectMultiScale(gray_scale, scaleFactor = 1.5, minNeighbors =5)
	for  (x, y, w, h) in faces:
		RGray = gray_scale[y:y+h, x:x+w]
		#compare the faces from live video frames to our trainer.yml
		id, confid = lbph_recognizer.predict(RGray)
		
        #if the confidence is less than 70 it will detect the face and unlock the servo lock
		if confid <= 70:
			try:
				while 1:
					p.ChangeDutyCycle(12.5)
			except keyboardInterrupt:
				pass
			GPIO.cleanup()
	cv2.imshow('frame', frame)
	key = cv2.waitKey(1)
	
	capture.truncate(0)
	
	if key == 27:
			break

cv2.destroyAllWindows()