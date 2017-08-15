from . import main
from flask import flash, redirect, render_template, session, url_for, abort


@main.route("/")
def index():
    return '<iframe style="width: 100%; height: 100%;" src="https://docs.google.com/document/d/11uYJ9BZKwesX4Mby7RkXV8SYH8X3PuQyI07_KBzkYSg/pub?embedded=true"></iframe>'
