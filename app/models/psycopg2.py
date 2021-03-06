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
	try:
		cursor.execute(query)
	except:
		cursor.execute('rollback;')
	results = cursor.fetchall()
	m_dic = {}
	for row in results:
		m_dic[row[0]] = row[1:]
	return jsonify(m_dic)


def all_main_q(query):
	try:
		cursor.execute(query)
	except:
		cursor.execute('rollback;')
	keys = [desc[0] for desc in cursor.description]
	keys.pop(0)   # remove the first element of the list as that is they dict key or id defined in the api
	results = cursor.fetchall()
	m_dic = {}
	for row in results:
		dic_id = row[0]
		temp_dic = dict(zip(keys, row[1:]))
		m_dic[dic_id] = temp_dic
	return m_dic


def all_q(query, keys):
	try:
		cursor.execute(query)
	except:
		cursor.execute('rollback;')
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
	try:
		cursor.execute(query)
	except:
		cursor.execute('rollback;')
	results = cursor.fetchall()
	m_dic = {}
	for row in results:
		m_dic[row[0]] = row[1]
	return jsonify(m_dic)


def point_in_zone_q(query):
	try:
		cursor.execute(query)
	except:
		cursor.execute('rollback;')
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


def all_table(query):
	try:
		cursor.execute(query)
	except:
		cursor.execute('rollback;')
	keys = [desc[0] for desc in cursor.description]
	results = cursor.fetchall()
	count = 0
	a_dict = {}
	for row in results:
		temp_dic = dict(zip(keys, row))
		a_dict[count] = temp_dic
		count += 1

	return a_dict


def dma(query):  # loq means list of queries
	r_dic = {}
	try:
		cursor.execute(query)
	except:
		cursor.execute('rollback;')
	results = cursor.fetchall()
	for row in results:
		json_acceptable_string = row[3].replace("'", "\"")
		d = json.loads(json_acceptable_string)
		coords = d.get("coordinates")
		row = ['' if v is None else v for v in row]   # avoid None type errors
		predLinks = [int(i) for i in row[14].split()]
		succLinks = [int(i) for i in row[17].split()]
		tmc = row[18]
		dic = {"_id": int(row[0]), "city": row[1], 'contain': [int(row[2])], 'coords': coords, 'fft': float(row[4]),
		       'firstOrientation': float(row[5]), 'fromNode': int(row[6]), 'gid': int(row[7]),
		       'id_parade': int(row[8]), 'lastOrientation': float(row[9]), 'length': float(row[10]),
		       'ltype': int(row[11]), 'name': row[12], 'numLanes': int(row[13]), 'predLinks': predLinks,
		       'reverse': [int(row[15])], 'speed': int(row[16]), 'succLinks': succLinks, 'tmc': tmc,
		       'toNode': int(row[19])}
		r_dic[int(row[0])] = dic


	return jsonify(r_dic)