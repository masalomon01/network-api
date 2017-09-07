import psycopg2 as pg
import psycopg2.extras
from urllib.parse import urlparse
from sqlalchemy.dialects import postgresql
from flask import (jsonify, make_response, abort, request, current_app)
import json
import math
import os
import urllib.parse
import json
from app import get_vars

conn = get_vars( os.getenv('CONFIG') or 'default', 'conn')
cursor = conn.cursor()
# dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def main_q(query):
	cursor.execute(query)
	results = cursor.fetchall()
	m_dic = {}
	for row in results:
		m_dic[row[0]] = row[1:]
	return jsonify(m_dic)


def all_q(query, keys):
	cursor.execute(query)
	results = cursor.fetchall()
	m_dic = {}
	for row in results:
		dic_id = row[0]
		temp_dic = dict(zip(keys, row[1:]))
		if 'geojson' in temp_dic:
			json_acceptable_string = temp_dic['geojson'].replace("'", "\"")
			d = json.loads(json_acceptable_string)
			# coords = d.get("coordinates")
			temp_dic['geojson'] = d
			city_letter = row[1][0]
			dic_id = city_letter.lower() + '_' + row[0]

		m_dic[dic_id] = temp_dic
	return m_dic


def main_q_one(query):
	cursor.execute(query)
	results = cursor.fetchall()
	m_dic = {}
	for row in results:
		m_dic[row[0]] = row[1]
	return jsonify(m_dic)


def point_in_zone_q(query):
	cursor.execute(query)
	results = cursor.fetchall()
	d = {}
	for row in results:
		if row[6] == 'Juarez':
			d['zone_id'] = row[5]
			d['city'] = row[6]
		elif row[6] == 'elpaso':
			d['zone_id'] = row[9]
			d['city'] = row[6]
	return jsonify(d)




