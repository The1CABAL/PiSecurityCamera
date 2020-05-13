
import Data.GlobalVars as cfg
from WebUI.VideoProcessing.Motion import *
from flask import Flask, Response, render_template
import argparse

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

if cfg.isRemote == 0:
	@app.route("/video_feed")
	def video_feed():
		# return the response generated along with the specific media type (mime type)
		return Response(generate(),
			mimetype = "multipart/x-mixed-replace; boundary=frame")
else:
	@app.route("/video_feed")
	def video_feed():
		return 'Hello World'

@app.route("/config")
def config():
	return render_template("config.html")
