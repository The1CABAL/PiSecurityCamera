
import Data.GlobalVars as cfg
from WebUI.VideoProcessing.Motion import *
from Classes.SQLITE import SQLITE as SQL
from flask import Flask, Response, render_template
import os
import sys

app = Flask(__name__)

@app.route("/")
def index():
	cam_dict = SQL.get_cams()
	return render_template(
		"index.html",
		cams = cam_dict
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

@app.route('/browser')
def browse():
    item_list = os.listdir(cfg.recordings + '/recordings')
    return render_template('browse.html', item_list=item_list)

@app.route("/submit_cams", methods = ['POST','GET'])
def submit_cams():
	SQL.insert_camera_ips()
	return render_template("config.html")