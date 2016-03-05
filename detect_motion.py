import cv2
import numpy as np 

from motion import Motion

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

camera = cv2.VideoCapture(0)
motion = Motion(snapFrame(camera))

while(camera.isOpened()):
 frame = snapFrame(camera)
 if motion.detectedMotion(frame):
  motion.paintDebug(frame)
 visualize(frame)
 if(shouldExit()):
  break

cleanup(camera)

