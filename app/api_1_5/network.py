from flask_restful import reqparse, Resource
from flask import request
#from ..models import (SQL_wkt, SQL_zone, SQL_census, SQL_main)
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
		zone_dict = {'traceid': 'linkid_parade', 'gid': 'gid'}
		col_list = ['zone']
		new_id = zone_dict[id]
		table = 'zones'
		sql = SQL_id_only(args["city"], new_id, table, col_list)
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


class nodes_API(Resource):


	def __init__(self):
		self.getParser = reqparse.RequestParser()
		self.getParser.add_argument("city", required=True)
		self.getParser.add_argument("attr", action="append")


	def get(self, id):
		args = self.getParser.parse_args()
		table = 'nodes'
		sql = SQL_main(args["city"], id, args["attr"], table)
		if  args["attr"] is None:
			query = sql.all_sql()
			result = all_main_q(query)
		else:
			query = sql.main_sql()
			result = main_q(query)

		return result



class angles_API(Resource):


	def __init__(self):
		self.getParser = reqparse.RequestParser()
		self.getParser.add_argument("city", required=True)


	def get(self):
		args = self.getParser.parse_args()
		table = 'angles'
		sql = SQL_noid(args["city"], table)
		query = sql.all_sql()
		result = all_table(query)

		return result



class featurePoints_API(Resource):


	def __init__(self):
		self.getParser = reqparse.RequestParser()
		self.getParser.add_argument("city", required=True)


	def get(self):
		args = self.getParser.parse_args()
		table = 'featurePoints'
		sql = SQL_noid(args["city"], table)
		query = sql.all_sql()
		result = all_table(query)

		return result



class dma_API(Resource):


	def __init__(self):
		self.getParser = reqparse.RequestParser()
		self.getParser.add_argument("link", action="append")


	def get(self, idType, cityCode):
		args = self.getParser.parse_args()
		table = 'wkt'
		sql = SQL_dma(cityCode, idType, args["link"], table)
		if  args["link"] is None:
			return make_response("please give me at least one link eg: &link=1", 400)
		else:
			query = sql.main_sql()  # loq stands for list of queries
			result = dma(query)

			return result



class info_API(Resource):


	def __init__(self):
		self.getParser = reqparse.RequestParser()
		self.getParser.add_argument("link", action="append")

	def get(self):
		table = 'deployment_info'
		sql = SQL_info(table)
		query = sql.active_network()
		result = all_table(query)

		return result



class quadTree_API(Resource):


	def __init__(self):
		self.getParser = reqparse.RequestParser()
		self.getParser.add_argument("city", required=True)


	def get(self):
		args = self.getParser.parse_args()
		table = 'quadtree'
		col_list = ['gid', 'cell_id']  # define the columns that you want
		sql = SQL_noid(args["city"], table, col_list)
		query = sql.some_col()
		result = main_q_one(query)

		return result



class poeSegments_API(Resource):


	def __init__(self):
		self.getParser = reqparse.RequestParser()
		self.getParser.add_argument("city", required=True)
		self.getParser.add_argument("attr", action="append")

	def get(self):
		args = self.getParser.parse_args()
		table = 'poesegments'
		group_var = 'segment_id, name, port_of_entry, direction, wt_entity_id, wt_seg_id'
		col_list = args["attr"]
		if args["attr"] is not None:
			for n, each in enumerate(col_list):
				if each == 'gid':
					col_list[n] = 'array_agg(gid) as gid'
				elif each == 'traceid':
					col_list[n] = 'array_agg(traceid) as traceid'
				else:
					pass
		all = 'segment_id, name, port_of_entry, direction, wt_entity_id, wt_seg_id, array_agg(gid) as gid, array_agg(traceid) as traceid'
		id = 'segment_id'
		sql = SQL_group(args["city"], table, group_var, all, id, col_list)
		if args["attr"] is None:
			query = sql.all_sql()
			result = all_main_q(query)
		else:
			query = sql.some_col()
			result = main_q(query)

		return result
