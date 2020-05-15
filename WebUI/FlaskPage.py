
import Data.GlobalVars as cfg
from WebUI.VideoProcessing.Motion import *
from Classes.SQLITE import SQLITE as SQL
from flask import Flask, Response, render_template
import sys

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/config")
def config():
	return render_template("config.html")

@app.route("/submit_cams", methods = ['POST','GET'])
def submit_cams():
	SQL.insert_camera_ips()
	return render_template("config.html")