from . import main
from flask import flash, redirect, render_template, session, url_for, abort, send_from_directory


@main.route("/")
def index():
	return '<iframe style="width: 100%; height: 100%;" src="https://docs.google.com/document/d/11uYJ9BZKwesX4Mby7RkXV8SYH8X3PuQyI07_KBzkYSg/pub?embedded=true"></iframe>'


@main.route("/loaderio-a7fd191577702f8371e9f349d4958a61.html")
def html_file():
	#return render_template(url_for('static', filename='loaderio-a7fd191577702f8371e9f349d4958a61.html'))
	return render_template('loaderio-a7fd191577702f8371e9f349d4958a61.html')
