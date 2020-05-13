
import Data.GlobalVars as cfg
from WebUI.FlaskPage import app, detect_motion

if __name__ == '__main__':
	cfg.isRemote = 1
	app.run(host='0.0.0.0', port=8000, debug=True,
		threaded=True, use_reloader=False)