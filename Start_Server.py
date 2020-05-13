
import Data.GlobalVars as cfg
from WebUI.FlaskPage import app, detect_motion
import imagezmq

ImageHub = imagezmq.ImageHub()

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

CONSIDER = set(["dog", "person", "car"])
objCount = {obj: 0 for obj in CONSIDER}
frameDict = {}

lastActive = {}
lastActiveCheck = datetime.now()

ESTIMATED_NUM_PIS = 4
ACTIVE_CHECK_PERIOD = 10
ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD

mW = args["montageW"]
mH = args["montageH"]
print("[INFO] detecting: {}...".format(", ".join(obj for obj in
	CONSIDER)))

while True:
	(rpiName, frame) = imageHub.recv_image()
	imageHub.send_reply(b'OK')

	if rpiName not in lastActive.keys():
		print("[INFO] receiving data from {}...".format(rpiName))

		lastActive[rpiName] = datetime.now()

		frame = imutils.resize(frame, width=400)
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
			0.007843, (300, 300), 127.5)

		net.setInput(blob)
		detections = net.forward()

		objCount = {obj: 0 for obj in CONSIDER}

		for i in np.arange(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]
			# filter out weak detections by ensuring the confidence is
			# greater than the minimum confidence
			if confidence > args["confidence"]:
				# extract the index of the class label from the
				# detections
				idx = int(detections[0, 0, i, 1])
				# check to see if the predicted class is in the set of
				# classes that need to be considered
				if CLASSES[idx] in CONSIDER:
					# increment the count of the particular object
					# detected in the frame
					objCount[CLASSES[idx]] += 1
					# compute the (x, y)-coordinates of the bounding box
					# for the object
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")
					# draw the bounding box around the detected object on
					# the frame
					cv2.rectangle(frame, (startX, startY), (endX, endY),
						(255, 0, 0), 2)
						# draw the sending device name on the frame

	cv2.putText(frame, rpiName, (10, 25),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	# draw the object count on the frame
	label = ", ".join("{}: {}".format(obj, count) for (obj, count) in
		objCount.items())
	cv2.putText(frame, label, (10, h - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)
	# update the new frame in the frame dictionary
	frameDict[rpiName] = frame
	# build a montage using images in the frame dictionary
	montages = build_montages(frameDict.values(), (w, h), (mW, mH))
	# display the montage(s) on the screen
	for (i, montage) in enumerate(montages):
		cv2.imshow("Home pet location monitor ({})".format(i),
			montage)
	# detect any kepresses
	key = cv2.waitKey(1) & 0xFF

		# if current time *minus* last time when the active device check
	# was made is greater than the threshold set then do a check
	if (datetime.now() - lastActiveCheck).seconds > ACTIVE_CHECK_SECONDS:
		# loop over all previously active devices
		for (rpiName, ts) in list(lastActive.items()):
			# remove the RPi from the last active and frame
			# dictionaries if the device hasn't been active recently
			if (datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:
				print("[INFO] lost connection to {}".format(rpiName))
				lastActive.pop(rpiName)
				frameDict.pop(rpiName)
		# set the last active check time as current time
		lastActiveCheck = datetime.now()
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
# do a bit of cleanup
cv2.destroyAllWindows()

#if __name__ == '__main__':
#	cfg.isRemote = 1
#	app.run(host='0.0.0.0', port=8000, debug=True,
#		threaded=True, use_reloader=False)