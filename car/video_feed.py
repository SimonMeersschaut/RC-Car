import cv2
import pickle


class CameraError(Exception):
  ...

camera_capture = None
RESOLUTION = (int(1280/5), int(720/5))

def initialize():
  global camera_capture
  if camera_capture is None:
    camera_capture = cv2.VideoCapture(0)
    print('initialized camera')

def is_ready():
  return camera_capture and camera_capture.isOpened()

def get_frame():
  ret, frame = camera_capture.read()
  if not ret:
    raise CameraError('Error in getting camera frame: ret was False.')
  frame = cv2.resize(frame, RESOLUTION, fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
  return pickle.dumps(frame)

def close():
  camera_capture.release()