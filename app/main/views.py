from . import main
from flask import flash, redirect, render_template, session, url_for, abort


@main.route("/")
def index():
    return "Traffic API is running!"