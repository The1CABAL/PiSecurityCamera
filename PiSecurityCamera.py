
import Data.GlobalVars as cfg
from WebUI.FlaskPage import app, detect_motion
from Classes.Startup import SetUp, get_settings
import threading

if __name__ == '__main__':

	SetUp()
	AppId, SelfStream, config_ip, config_port = get_settings()

	if AppId == '0':
		# start a thread that will perform motion detection
		t = threading.Thread(target=detect_motion, args=([59]))
		t.daemon = True
		t.start()

		# start the flask app
		app.run(host='0.0.0.0', port=8000, debug=True,
			threaded=True, use_reloader=False)
	elif AppId == '1':
		# start a thread that will perform motion detection
		#t = threading.Thread(target=detect_motion, args=([59]))
		#t.daemon = True
		#t.start()
		print('Listening Thread Runs here')

		# start the flask app
		app.run(host='0.0.0.0', port=8000, debug=True,
			threaded=False, use_reloader=False)
	elif AppId == '2':
		print("AppId 2")
