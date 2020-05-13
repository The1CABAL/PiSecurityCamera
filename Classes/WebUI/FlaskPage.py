
from Classes.WebUI.VideoProcessing.Motion import *
from flask import Flask, Response, render_template
import argparse

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
