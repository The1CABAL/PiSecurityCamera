
import cv2
import numpy as np
import socket
import sys
import pickle
import struct
cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.16',8089))
while True:
    ret,frame=cap.read()
    data = pickle.dumps(frame)
    clientsocket.sendall(struct.pack("H", len(data))+data)