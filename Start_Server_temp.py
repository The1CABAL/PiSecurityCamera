
'''
This File is here as a temporary workaround for getting the testing 
environment working until we can find a way to reload the site once the 
configurations are changed. 
'''

import Data.GlobalVars as cfg
from WebUI.FlaskPage import app, detect_motion
from Classes.Startup import SetUp, get_settings
import threading

import sqlite3

if __name__ == '__main__':

	SetUp()
	conn = cfg.conn
	c = conn.cursor()
	c.execute('UPDATE Config SET KeyValue = 1 WHERE KeyName = "ApplicationId"')
	conn.commit()
	c.close()
	AppId, SelfStream, config_ip, config_port = get_settings()

	if AppId == '0':
		# start a thread that will perform get video from camera
		t = threading.Thread(target=detect_motion, args=([59]))
		t.daemon = True
		t.start()

		# start the flask app
		app.run(host='0.0.0.0', port=8000, debug=True,
			threaded=True, use_reloader=False)
	elif AppId == '1':
		cfg.isRemote = 1
		# start a thread that will listen for video input
		t = threading.Thread(target=detect_motion, args=([59]))
		t.daemon = True
		t.start()
		print('Listening Thread Runs here')

		# start the flask app
		app.run(host='0.0.0.0', port=8000, debug=True,
			threaded=False, use_reloader=False)
	elif AppId == '2':
		print("AppId 2")