
import Data.GlobalVars as cfg
from WebUI.VideoProcessing.Motion import *
from Classes.SQLITE import SQLITE as SQL
from flask import Flask, Response, render_template, abort
import os
import sys

app = Flask(__name__)

@app.route("/")
def index():
	cam_dict = SQL.get_cams()
	return render_template(
		"index.html",
		dict_set = zip(cam_dict)
		)

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/config")
def config():
	cam_dict = SQL.get_cams()
	return render_template(
		"config.html",
		dict_set = zip(cam_dict)
		)

@app.route('/browser', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def browse(req_path):
	base_dir = cfg.recordings + '\\recordings'
	abs_path = os.path.join(base_dir, req_path)

	if not os.path.exists(abs_path):
		return abort(404)

	if os.path.isfile(abs_path):
		return send_file(abs_path)

	files = os.listdir(abs_path)
	return render_template('browse.html', files=files, path=abs_path)

@app.route("/submit_cams", methods = ['POST','GET'])
def submit_cams():
	SQL.insert_camera_ips()
	return render_template("config.html")