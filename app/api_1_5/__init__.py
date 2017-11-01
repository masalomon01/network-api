from flask import Blueprint
from flask_restful import Api
from .network import *
# from .network import wkt_API, zone_API, census_API, nodes_API, angles_API, featurePoints_API, dma_API


api_bp = Blueprint('api v1.5', __name__)
api = Api(api_bp)

api.add_resource(wkt_API, '/network/<id>')
api.add_resource(zone_API, '/zone/<id>')
api.add_resource(census_API, '/census')
api.add_resource(nodes_API, '/nodes/<id>')
api.add_resource(angles_API, '/angles')
api.add_resource(featurePoints_API, '/featurePoints')
api.add_resource(dma_API, '/dma/<idType>/<cityCode>')
api.add_resource(info_API, '/network/info')
api.add_resource(quadTree_API, '/quadtree')
api.add_resource(poeSegments_API, '/poesegments')




