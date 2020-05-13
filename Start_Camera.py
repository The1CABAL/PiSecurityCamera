
import Data.GlobalVars as cfg
try:
    import PiCamera
    cfg.isPi = 1
except:
    cfg.isPi = 0

from imutils.video import VideoStream
import imagezmq
import socket
import time

ip = input("Input Server IP Address: ")
sender = imagezmq.ImageSender(connect_to="tcp://"+ip+":8000")
rpiName = socket.gethostname()

if cfg.isPi == 1:
    vs = VideoStream(usePiCamera=True)
else:
    vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    frame = vs.read()
    sender.send_image(rpiName, frame)