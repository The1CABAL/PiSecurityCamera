
import Data.GlobalVars as cfg
from Classes.Camera import FaceMotionDetector
from imutils.video import VideoStream
import imagezmq
import threading
import datetime
import imutils
import time
import cv2

# initialize the output frame and a lock 
outputFrame = None
lock = threading.Lock()

# initialize the video stream
if cfg.isPi == 1:
	vs = VideoStream(usePiCamera=1).start()
else: 
	vs = VideoStream(src=0).start()
time.sleep(2.0)

def place_frame(faceCascade, isPi, image, gray, rawCapture = ''):
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
        )

    #Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

def detect_motion(frameCount):
	faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
	global vs, outputFrame, lock

	md = FaceMotionDetector(accumWeight=0.1)
	total = 0

	# loop over frames from the video stream
	while True:
		# read the next frame from the video stream and normalize it
		if cfg.isRemote == 0:
			frame = vs.read()
		elif cfg.isRemote == 1:
			image_hub = imagezmq.ImageHub(open_port='tcp://127.0.0.1:5555')
			rPi_name, image = image_hub.recv_image()

		frame = imutils.resize(frame, width=400)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (7, 7), 0)

		place_frame(faceCascade, cfg.isPi, frame, gray)

		# grab the current timestamp and draw it on the frame
		timestamp = datetime.datetime.now()
		cv2.putText(frame, timestamp.strftime(
			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		# if the total number of frames has reached a sufficient number to construct a reasonable background model, then continue to process the frame
		if total > frameCount:
			# detect motion in the image
			motion = md.detect(gray)

			# cehck to see if motion was found in the frame
			if motion is not None:
				# unpack the tuple and draw the box surrounding the "motion area" on the output frame
				(thresh, (minX, minY, maxX, maxY)) = motion
				cv2.rectangle(frame, (minX, minY), (maxX, maxY),
					(0, 0, 255), 2)
				#record()

		# update the background model and increment the total number of frames read thus far
		md.update(gray)
		total += 1
		# acquire the lock, set the output frame, and release the lock
		with lock:
			outputFrame = frame.copy()
		
def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock

	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip the iteration of the loop
			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')