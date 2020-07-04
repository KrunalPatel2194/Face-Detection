#importing all required libraries
import cv2
import numpy as np
import os
from PIL import Image
import pickle
#using haarcascade frontal face detection pretrained model 
front_face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#using LBPHF(Local Binary Patterns Histogram) from OpenCV as a recognizer
lbph_recognizer = cv2.face.createLBPHFaceRecognizer()

#scan into each image directory and if the images are present, image is converted into NumPy array
face_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(face_dir, "face_img")

c_id = 1
l_id = {}
yLabels = []
xTrain = []

#performs the face detection again to make sure that we have the right images and then prepare the training data
for root, dirs, files in os.walk(image_dir):
		print(root, dirs, files)
		for file in files:
				print(file)
                #once it takes the image it creates a label file and store all the names of the image in the label file
				if file.endswith("png") or file.endswith("jpg"):
						path = os.path.join(root, file)
						label = os.path.basename(root)
						print(label)
						
						if not label in l_id:
								l_id[label] = c_id
								print(l_id)
								c_id += 1
								
						id = l_id[label]
						pilImage = Image.open(path).convert("L")
						imageArray = np.array(pilImage, "uint8")
						faces = front_face_cascade.detectMultiScale(imageArray, scaleFactor=1.1, minNeighbors=5)
						
						for (x, y, w, h) in faces:
							roi = imageArray[y:y+h, x:x+w]
							xTrain.append(roi)
							yLabels.append(id)
								
with open("labels", "wb") as f:
		pickle.dump(l_id, f)
		f.close()
#initiating training and save the trainer.yml file in the local working directory
lbph_recognizer.train(xTrain, np.array(yLabels))
lbph_recognizer.save("train.yml")
print(l_id)