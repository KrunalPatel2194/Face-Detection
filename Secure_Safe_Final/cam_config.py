#importing libraries
import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np

#initializing video camera class for pi camera
class VideoCamera(object):
    
    #initializing camera
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()
    #defining flip function to flip the camera frame
    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame
    #get the frames from pi camera
    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    #get the object classification from frame
    def get_object(self, classifier):
        found_objects = False
        frame = self.flip_if_needed(self.vs.read()).copy() 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(objects) > 0:
            found_objects = True

        #draw a green rectangle around the objects
        for (x, y, w, h) in objects:
           cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return (jpeg.tobytes(), found_objects)


