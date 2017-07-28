from flask_restful import reqparse, Resource
from flask import request
from ..models import (SQL_wkt, SQL_zone)
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
