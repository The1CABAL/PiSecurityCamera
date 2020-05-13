
import Data.GlobalVars as cfg
try:
    import PiCamera
    cfg.isPi = 1
except:
    cfg.isPi = 0

import socket
import time
from imutils.video import VideoStream
import imagezmq

ip = input("Input Server IP Address: ")
sender = imagezmq.ImageSender(connect_to='tcp://'+ip+':5555')
 
rpi_name = socket.gethostname() # send RPi hostname with each image
picam = VideoStream(usePiCamera=True).start()
time.sleep(2.0)  # allow camera sensor to warm up
while True:  # send images as stream until Ctrl-C
    image = picam.read()
    sender.send_image(rpi_name, image)