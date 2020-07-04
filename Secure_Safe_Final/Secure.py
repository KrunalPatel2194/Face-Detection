#importing all required libraries
import cv2
import sys
from email_code import sendEmail
from flask import Flask, render_template, Response
from cam_config import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading

#set email interval for 5 second
email_interval = 500

#initializing camera module, resolution, framerate and raw capture size
v_camera = VideoCamera(flip=False)

#using Haar cascade model for frontal object detection
obj_clsfr = cv2.CascadeClassifier("facial_recognition_model.xml")

#creating a python app for camera
py_app = Flask(__name__)

epoch = 0
#Pi camera is continuously recording the frames and checking for object, here object is a face
def check_for_objects():
		global epoch
		while True:
				try:    #if the object is detected, then it capture that frame and will execute the send email 
						frame, obj = v_camera.get_object(obj_clsfr)
						if obj and (time.time() - epoch) > email_interval:
								epoch = time.time()
								print ("Trying to send email")
								sendEmail(frame)
								print ("Done")
				except:
						print("Error", sys.exc_info()[0])

#launching the app						
if __name__ == '__main__':
	t = threading.Thread(target=check_for_objects, args=())
	t.daemon = True
	t.start()
	py_app.run()
								