
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    isPi = 1
except:
    isPi = 0
import cv2
import time

class FaceDetector():

    def __init__(self):
        self.Detection_Main()

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

    def Detection_Main(self):

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        if isPi == 1:
            camera = PiCamera()
            camera.framerate = 32
            camera.rotation = 180
            rawCapture = PiRGBArray(camera)

            time.sleep(0.1)
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

                #Capture Video
                image = frame.array
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                place_frame(faceCascade, isPi, image, gray, rawCapture)
                rawCapture.truncate(0)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            webcam = cv2.VideoCapture(0)
            while True:
                _, image = webcam.read()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                self.place_frame(faceCascade, isPi, image, gray)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break