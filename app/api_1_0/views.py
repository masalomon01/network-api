from . import api
from .. import db
import datetime
import os
import json
import math
from urllib.parse import urlparse
from sqlalchemy.dialects import postgresql
import psycopg2 as pg
import psycopg2.extras
from flask import (jsonify, make_response, abort, request, current_app)
from app import get_vars
# from flask_cors import CORS, cross_origin

# url = urlparse('postgres://dtolyqrislafqi:5a3d4791e40522df04870a9fb280348eac48e6bffb799095000b2305b61cbbbc@ec2-23-23-228-115.compute-1.amazonaws.com:5432/d9crmiih79tddt')
# db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
# schema = 'dev_wkts'
# conn = pg.connect(db)
# conn = pg.connect(user='postgres', password='postgres', host='192.168.1.98', database='wkt')  # dev port default 5432
# cursor = conn.cursor()
conn = get_vars( os.getenv('CONFIG') or 'default', 'conn')
schema = get_vars( os.getenv('CONFIG') or 'default', 'schema')
cursor = conn.cursor()
# dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


"""""
"API"
"""""


@api.route('/mario/test', methods=['GET'])
def mario_test():
	# return 100 lines of the wkt file
	links = request.args.get('links')
	# links is required
	if links is None:
		return make_response("you need to give me a number of links to return", 400)
	else:
		test = get_some_links(links)
		return test


@api.route('/mario/radius', methods=['GET'])
def mario_radius():
	# return links around a radius
	lon, lat = request.args.get('lon'), request.args.get('lat')
	radius = request.args.get('radius')
	if lat is None or lon is None or radius is None:
		respo = "You need to have values for " + "lat " + lat + "lon " + lon + "radius " + radius
		return make_response(respo, 400)
	else:
		result = get_links_from_radius(lon, lat, radius)
		return result


@api.route('/network/trace', methods=['GET'])
def trace_network():
	# trace will ask for a city and api needs to return links, predecessors and successors
	city = request.args.get('city')
	if city is None:
		return make_response("please give me a city to return the correct data tucson, elpaso, austin", 400)
	else:
		trace = get_pred_suc(city)
		return trace


@api.route('/network/idmapping/', methods=['GET'])
#@cross_origin() # allow all origins all methods.
def gid_linkid_mapping():   # this will provide a mapping dictionary for linkid and gid for a specific city
	city = request.args.get('city')
	if city is None:
		return make_response("please give me a city to return the correct data tucson, elpaso, austin", 400)
	else:
		mapping = get_id_mapping(city)
		return mapping


@api.route('/network/tmc', methods=['GET'])
def network_tmc():
	# this will return tmc id: and all the associated [gid, length] to that tmc
	city = request.args.get('city')
	if city is None:
		return make_response("please give me a city to return the correct data tucson, elpaso, austin", 400)
	else:
		tmc = get_tmc(city)
		return tmc


@api.route('/network/link/<cityCode>/<int:id>')
#@cross_origin() # allow all origins all methods.
def get_link(cityCode, id):
	city = cityCode
	gid = id
	link = get_dma(city, gid)
	if link is None:
		return make_response("link not found", 404)
	return link


"""
HELPERS
"""


def get_some_links(links):
	query = "SELECT * FROM {}.dev_wkts_tucson LIMIT {};".format(schema, links)
	cursor.execute(query)
	results = cursor.fetchall()
	t_dict = {}
	for row in results:
		t_dict[row[0]] = {"gid": row[0], "wkt": row[2], "length": row[5], 'speed': row[6], 'ltype': row[7],
					'primaryName': row[8]}
	return jsonify(t_dict)


def get_links_from_radius(lon, lat, radius):
	#conn = pg.connect(user='networkland', password='M+gis>ptv',
	#                  host='postgresql.crvadswmow49.us-west-2.rds.amazonaws.com',
	#                  database='Networkland')  # port default 5432
	#cursor = conn.cursor()
	query = """SELECT gid, street_name, speed, direction FROM tucson
				WHERE ST_DWithin(ST_StartPoint(geom)::geography, 
				ST_GeomFromText('POINT({} {})',4269)::geography, {}) 
				LIMIT 100;""".format(lon, lat, radius)
	cursor.execute(query)
	results = cursor.fetchall()
	r_dic = {}
	for row in results:
		r_dic[row[0]] = {"gid": row[0], "street_name": row[1], 'speed': row[2], 'direction': row[3]}
	return jsonify(r_dic)


def get_pred_suc(city):
	query = """SELECT linkid_ptv, predecessors, successors
                FROM {}.wkt_{}""".format(schema, city)
	cursor.execute(query)
	results = cursor.fetchall()
	t_dic = {}
	for row in results:
		t_dic[row[0]] = [row[1], row[2]]
	return jsonify(t_dic)


def get_id_mapping(city):
	query = """SELECT linkid_parade, linkid_ptv
                FROM {}.wkt_{}""".format(schema, city)
	cursor.execute(query)
	results = cursor.fetchall()
	m_dic = {}
	for row in results:
		m_dic[row[0]] = row[1]
	return jsonify(m_dic)


def get_tmc(city):
	query = """SELECT tmc, array_agg('[' || linkid_parade || ', ' || length || ']')
                FROM {}.wkt{}
                WHERE tmc is not NULL
                GROUP BY tmc""".format(schema, city)
	cursor.execute(query)
	results = cursor.fetchall()
	t_dic = {}
	for row in results:
		t_dic[row[0]] = row[1]
	return jsonify(t_dic)


def get_dma(city, gid):
	query = """ SELECT linkid_parade, '{}' as city, linkid_parade as contain, ST_AsGeoJSON(geom),
            fftt, firstorientation, fromnodeid_parade, linkid_ptv, linkid_parade, lastorientation, length, 
            new_ltype, primaryname, numlanes, predecessors, reverseid_parade, speed, successors, tmc, tonodeid_parade
            FROM {}.wkt_{}
            WHERE linkid_ptv = '{}'
            GROUP BY linkid_ptv, fftt, firstorientation, fromnodeid_parade, linkid_ptv, linkid_parade, lastorientation, 
            length, new_ltype, primaryname, numlanes, predecessors, reverseid_parade, speed, successors, tmc, 
            tonodeid_parade""".format(city, schema, city, gid)
	cursor.execute(query)
	results = cursor.fetchall()
	print(results)
	#dict_cur.execute(query)
	#results = dict_cur.fetchone()
	print(results)
	for row in results:
		json_acceptable_string = row[3].replace("'", "\"")
		d = json.loads(json_acceptable_string)
		coords = d.get("coordinates")
		predLinks = [int(i) for i in row[14].split()]
		succLinks = [int(i) for i in row[17].split()]
		if not row[18]:
			tmc = ""
		else:
			tmc = row[18]
		dic = {"_id": int(row[0]), "city": row[1], 'contain': [int(row[2])], 'coords': coords, 'fft': float(row[4]),
		       'firstOrientation': float(row[5]), 'fromNode': int(row[6]), 'gid': int(row[7]),
		       'id_parade': int(row[8]), 'lastOrientation': float(row[9]), 'length': float(row[10]),
		       'ltype': int(row[11]), 'name': row[12], 'numLanes': int(row[13]), 'predLinks': predLinks,
		       'reverse': [int(row[15])], 'speed': int(row[16]), 'succLinks': succLinks, 'tmc': tmc,
		       'toNode': int(row[19])}
	return jsonify(dic)
