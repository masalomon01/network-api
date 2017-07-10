from . import api
from .. import db
import datetime
import os
import json
import math
from urllib.parse import urlparse
from sqlalchemy.dialects import postgresql
import psycopg2 as pg
from flask import (
    jsonify, make_response, abort, request, current_app
)

url = urlparse('postgres://dtolyqrislafqi:5a3d4791e40522df04870a9fb280348eac48e6bffb799095000b2305b61cbbbc@ec2-23-23-228-115.compute-1.amazonaws.com:5432/d9crmiih79tddt')
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
schema = 'dev_wkts'
conn = pg.connect(db)
cursor = conn.cursor()


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


@api.route('/trace', methods=['GET'])
def trace_network():
    # trace will ask for a city and api needs to return links, predecessors and successors
    city = request.args.get('city')
    if city is None:
        return make_response("please give me a city to return the correct data tucson, elpaso, austin", 400)
    else:
        trace = get_pred_suc(city)
        return trace


@api.route('/idmapping', methods=['GET'])
def gid_linkid_mapping():
    # this will provide a mapping dictionary for linkid and gid for a specific city
    city = request.args.get('city')
    if city is None:
        return make_response("please give me a city to return the correct data tucson, elpaso, austin", 400)
    else:
        mapping = get_id_mapping(city)
        return mapping


"""
HELPERS
"""

def connect_2_db():
	conn = pg.connect(user='networkland', password='M+gis>ptv',
	                  host='postgresql.crvadswmow49.us-west-2.rds.amazonaws.com',
	                  database='Networkland')  # port default 5432
	return conn

def get_some_links(links):
	# conn = pg.connect(user='postgres', password='postgres', host='192.168.1.98', database='wkt')  # port default 5432
	#conn = connect_2_db()
	#cursor = conn.cursor()
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
                FROM {}.dev_wkts_{}""".format(schema, city)
    cursor.execute(query)
    results = cursor.fetchall()
    t_dic = {}
    for row in results:
        t_dic[row[0]] = [row[1], row[2]]
    return jsonify(t_dic)


def get_id_mapping(city):
    query = """SELECT linkid_parade, linkid_ptv
                FROM {}.dev_wkts_{}""".format(schema, city)
    cursor.execute(query)
    results = cursor.fetchall()
    m_dic = {}
    for row in results:
        m_dic[row[0]] = row[1]
    return jsonify(m_dic)
