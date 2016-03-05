import cv2
import os
import pprint 

WORKING_DIR = './videos'
CAPTURES_DIR = './captures'
TIME_THRESHOLD_SECONDS = 5
FPS = 5

def mkdir(path):
 if not os.path.exists(path):
  os.makedirs(path)

def frameFilepath(framePath):
 return os.path.join(CAPTURES_DIR, framePath)
 
def filepath(grouping):
 return os.path.join(WORKING_DIR, grouping)

def getListOfCaptures():
 captures =[f for f in os.listdir(CAPTURES_DIR) if '.jpg' in f]
 captures.sort()
 return captures

def getCaptureGroupings():
 groupings = {} 
 captures = getListOfCaptures()
 lastGroup = ""
 for c in captures:
  (date, time, seconds) = c.split('.')[0].split('-')
 
  if lastGroup in groupings:
   groupings[lastGroup].append(c)
  else:
   lastGroup = '-'.join([date])
   groupings[lastGroup] = [c]

 print groupings
 return groupings

def lazyVideoWriter(group, frame):
 path = filepath(group) + '.avi'
 (h,w,layers) = frame.shape
 fourcc = cv2.cv.CV_FOURCC(*'MJPG')
 return cv2.VideoWriter(path, fourcc, FPS, (w, h))

mkdir(WORKING_DIR)

for group, framePaths in getCaptureGroupings().iteritems():
 video = None
 path = filepath(group)
 for framePath in framePaths:
  frame = cv2.imread(frameFilepath(framePath))
  if not video:
   video = lazyVideoWriter(group, frame)
  video.write(frame)
 print video
 video.release()

