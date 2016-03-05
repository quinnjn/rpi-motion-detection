import cv2
import numpy as np 
import os
from time import time
from datetime import datetime
from fake import g
from motion import Motion

WORKING_DIR = './captures'
TIMESTAMP_FORMAT = '%Y%m%d-%H%M%S-%f'

def mkdir(path):
 if not os.path.exists(path):
  os.makedirs(path)

def timestamp():
 return datetime.fromtimestamp(time()).strftime(TIMESTAMP_FORMAT)
 
def filepath():
 return os.path.join(WORKING_DIR, "%s.jpg" % timestamp())

def snapFrame(camera):
 """
 Returns a frame form the camera.
 """
 return camera.read()[1]

def visualize(frame):
 """
 Visualizes a frame.
 """
 cv2.imshow('frame', frame)

def shouldExit():
 # TODO figure this out
 return cv2.waitKey(1) & 0xFF == ord('q')

def cleanup():
 """
 Prepare for shutting down.
 """
 cv2.release()
 cv2.destroyAllWindows()

mkdir(WORKING_DIR)

camera = cv2.VideoCapture(0)
motion = Motion(snapFrame(camera))

while(camera.isOpened()):
 frame = snapFrame(camera)
 if motion.detectedMotion(frame):
  cv2.imwrite(filepath(), frame)
  motion.paintDebug(frame)
 visualize(frame)
 if(shouldExit()):
  break

cleanup(camera)

