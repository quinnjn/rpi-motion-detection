import cv2
import numpy as np 

BLURING_KERNEL_SIZE = 10 # TODO optimize this value 
THRESHOLD_SENSITIVITY = 30 # TODO optimize this value

def getRectangleOfInterest(frame):
 """
 Gets back the area that we are interested in watching.
 """
 y1 = 200
 y2 = 300
 x1 = 200
 x2 = 300
 return frame[y1:y2, x1:x2]

def snapFrame(camera):
 """
 Returns a frame form the camera.
 """
 return camera.read()[1]

def normalize(frame):
 """
 Puts the frame into a calculative state.
 """
 return gray(shrink(frame))

def shrink(frame):
 """
 Return a smaller frame to run calculations on.
 """
 return frame #TODO fix getRectangleOfInterest(frame)

def gray(frame):
 """
 Grayscale the frame to make math faster?
 """
 return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def difference(old, new):
 """
 Calculates a difference between two frames.
 """
 return threshold(blur(absdiff(old, new))) 

def absdiff(old, new):
 """
 Returns an absolute difference tbween two frames.
 """
 return cv2.absdiff(old, new)

def blur(frame):
 """
 Blurs a frame. Useful for filtering out a noisy image?
 """
 return cv2.blur(frame, (BLURING_KERNEL_SIZE, BLURING_KERNEL_SIZE))

def threshold(frame):
 """
 Filters out 'boring' pixels from the frame.
 """
 # TODO what is param 255?
 return cv2.threshold(frame, THRESHOLD_SENSITIVITY, 255, cv2.THRESH_BINARY)[1]  

def findContours(frame):
 """
 Finds shapes inside the frame.
 """
 return cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

def detectMotion(contours):
 """
 Checks contours for movement.
 """
 # If there are any contours, it means there is movement.
 return len(contours) > 0

def boundMovements(frame, contours):
 """
 Returns bounding boxes around movement.
 """
 for c in contours:
  (x,y,w,h) = cv2.boundingRect(c)
  p1 = (x,y)
  p2 = (x+w, y+h)
  cv2.rectangle(frame, p1, p2, (0,255,0), 1)

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

previousFrame = None

camera = cv2.VideoCapture(0)

while(camera.isOpened()):
 if(previousFrame == None):
  previousFrame = normalize(snapFrame(camera))

 currentFrame = snapFrame(camera)
 frame = normalize(currentFrame)
 differenceFrame = difference(previousFrame, frame)
 contours = findContours(differenceFrame)
 detectedMotion = detectMotion(contours)

 if detectedMotion:
   boundMovements(currentFrame, contours)
 visualize(currentFrame)

 # We dont need previousFrame anymore, set it as current frame
 previousFrame = frame

 if(shouldExit()):
  break
  
cleanup(camera)
