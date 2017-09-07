from flask import Blueprint
from flask_restful import Api
from .network import wkt_API, zone_API, census_API, nodes_API, angles_API, featurePoints_API


api_bp = Blueprint('api v1.5', __name__)
api = Api(api_bp)

api.add_resource(wkt_API, '/network/<id>')
api.add_resource(zone_API, '/zone/<id>')
api.add_resource(census_API, '/census')
api.add_resource(nodes_API, '/nodes/<id>')
api.add_resource(angles_API, '/angles')
api.add_resource(featurePoints_API, '/featurePoints')



