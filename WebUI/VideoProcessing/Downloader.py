
import vlc
import time
import cv2
import os.path

def record():
    vid_len=0
    vlcInstance = vlc.Instance("--demux=ts")
    player1 = vlcInstance.media_player_new()
    media1 = vlcInstance.media_player_new("http://localhost:8000/video_feed")
    #media1.add_option("sout=file/ts:sample.mpg")
    player1.set_media(media1)

    player1.play()

    while vid_len < 30:
        time.sleep()
        if os.path.isfile('sample.mp4') and (os.path.getsize('sample.mp4') > 0):
            video_file = cv2.VideoCapture('sample.mp4')
            frames = int(video_file.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = (video_file.get(cv2.CAP_PROP_FPS))
            vid_len = frames/fps

    player1.stop()
    media1.release()