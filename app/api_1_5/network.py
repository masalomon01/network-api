from flask_restful import reqparse, Resource
from flask import request
from ..models import (SQL_wkt, SQL_zone, SQL_census)
from ..models import *


class wkt_API(Resource):


	def __init__(self):
		self.getParser = reqparse.RequestParser()
		self.getParser.add_argument("city", required=True)
		self.getParser.add_argument("attr", action="append")


	def get(self, id):
		args = self.getParser.parse_args()
		sql = SQL_wkt(args["city"], id, args["attr"])
		if  args["attr"] is None:
			query, keys = sql.all_sql()
			result = all_q(query, keys)
		else:
			query = sql.main_sql()
			result = main_q(query)

		return result


class zone_API(Resource):


	def __init__(self):
		self.getParser = reqparse.RequestParser()
		self.getParser.add_argument("city", required=True)


	def get(self, id):
		args = self.getParser.parse_args()
		sql = SQL_zone(args["city"], id)
		query = sql.main_sql()
		result = main_q_one(query)

		return result


class census_API(Resource):


	def __init__(self):
		self.getParser = reqparse.RequestParser()
		self.getParser.add_argument("city", required=True)
		self.getParser.add_argument('lat', type=float, default=0.0)
		self.getParser.add_argument('lon', type=float, default=0.0)



	def get(self):
		args = self.getParser.parse_args()
		sql = SQL_census(args["city"], args["lat"], args["lon"])
		if args["lat"] == 0.0 and args["lon"] == 0.0:
			query, keys = sql.main_sql()
			result = all_q(query, keys)
		else:
			query = sql.point_in_zone()
			result = point_in_zone_q(query)

		return result