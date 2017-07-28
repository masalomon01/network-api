from flask import Blueprint

api = Blueprint('api v1', __name__)

from .views import *  # noqa
