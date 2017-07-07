
from flask import flash, redirect, render_template, session, url_for, abort


@main.route("/", methods=['GET', "POST"])
def index():
    return "Traffic API is running!"