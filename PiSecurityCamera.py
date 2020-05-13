
import Data.GlobalVars as cfg
from WebUI.FlaskPage import app, detect_motion
import threading

if __name__ == '__main__':

	# start a thread that will perform motion detection
	t = threading.Thread(target=detect_motion, args=([59]))
	t.daemon = True
	t.start()

	# start the flask app
	app.run(host='0.0.0.0', port=8000, debug=True,
		threaded=True, use_reloader=False)