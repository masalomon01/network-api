from flask import Blueprint
from flask_restful import Api
from .network import wkt_API, zone_API


api_bp = Blueprint('api v1.5', __name__)
api = Api(api_bp)

api.add_resource(wkt_API, '/network/<id>')
api.add_resource(zone_API, '/zone/<id>')

