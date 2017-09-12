from . import main
from flask import flash, redirect, render_template, session, url_for, abort, send_from_directory


@main.route("/")
def index():
	return '<iframe style="width: 100%; height: 100%;" src="https://docs.google.com/document/d/11uYJ9BZKwesX4Mby7RkXV8SYH8X3PuQyI07_KBzkYSg/pub?embedded=true"></iframe>'

# app = Flask(__name__, main='main')
@main.route("/loaderio-a7fd191577702f8371e9f349d4958a61.txt")
def txt_file():
	return redirect(url_for('main.txt_file', filename='loaderio-a7fd191577702f8371e9f349d4958a61.txt'))
