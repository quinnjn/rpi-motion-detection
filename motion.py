import cv2
import numpy as np 

class Motion():
 
 def __init__(self, frame):
  self.BLURING_KERNEL_SIZE = 10 # TODO optimize this value 
  self.THRESHOLD_SENSITIVITY = 30 # TODO optimize this value

  self.previousFrame = self.normalize(frame)
  self.previousContours = []

 def detectedMotion(self, currentFrame):
  normalizedFrame = self.normalize(currentFrame.copy())
  frame = self.difference(self.previousFrame, normalizedFrame)
  self.contours = self.findContours(frame)
  # We dont need previousFrame anymore, set it as normalized frame
  self.previousFrame = normalizedFrame
  return len(self.contours) > 0

 def paintDebug(self, frame):
  self.applyContoursToFrame(frame, self.contours)
 
 def normalize(self, frame):
  """
  Puts the frame into a calculative state.
  """
  return self.gray(self.shrink(frame))
 
 def shrink(self, frame):
  """
  Return a smaller frame to run calculations on.
  """
  return frame #TODO fix getRectangleOfInterest(frame)
 
 def gray(self, frame):
  """
  Grayscale the frame to make math faster?
  """
  return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
 def difference(self, old, new):
  """
  Calculates a difference between two frames.
  """
  return self.threshold(self.blur(self.absdiff(old, new))) 
 
 def absdiff(self, old, new):
  """
  Returns an absolute difference tbween two frames.
  """
  return cv2.absdiff(old, new)
 
 def blur(self, frame):
  """
  Blurs a frame. Useful for filtering out a noisy image?
  """
  return cv2.blur(frame, (self.BLURING_KERNEL_SIZE, self.BLURING_KERNEL_SIZE))
 
 def threshold(self, frame):
  """
  Filters out 'boring' pixels from the frame.
  """
  # TODO what is param 255?
  return cv2.threshold(frame, self.THRESHOLD_SENSITIVITY, 255, cv2.THRESH_BINARY)[1]  
 
 def findContours(self, frame):
  """
  Finds shapes inside the frame.
  """
  return cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
 
 def applyContoursToFrame(self, frame, contours):
  """
  Paints bounding boxes around movement to frame.
  """
  for c in contours:
   (x,y,w,h) = cv2.boundingRect(c)
   p1 = (x,y)
   p2 = (x+w, y+h)
   cv2.rectangle(frame, p1, p2, (0,255,0), 1)
 
