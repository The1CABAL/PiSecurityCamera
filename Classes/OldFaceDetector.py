
import Data.GlobalVars as cfg
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    cfg.isPi = 1
except:
    cfg.isPi = 0
import cv2
import time

class FaceDetector():

    def __init__(vs):
        self = FaceDetector
        self.Detection_Main(self, vs)

    def place_frame(self, faceCascade, isPi, image, gray, rawCapture = ''):
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

        #Display the resulting frame
        cv2.imshow('Frame', image)

    def Detection_Main(self, vs):

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        if cfg.isPi == 1:
            vs

            time.sleep(0.1)
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

                #Capture Video
                image = frame.array
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                self.place_frame(faceCascade, isPi, image, gray, rawCapture)
                rawCapture.truncate(0)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            vs
            while True:
                _, image = vs.read()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                self.place_frame(faceCascade, cfg.isPi, image, gray)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break