import psycopg2 as pg
import psycopg2.extras
from urllib.parse import urlparse
from sqlalchemy.dialects import postgresql
from flask import (jsonify, make_response, abort, request, current_app)
import json
import math

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
'''
url = urlparse('postgres://dtolyqrislafqi:5a3d4791e40522df04870a9fb280348eac48e6bffb799095000b2305b61cbbbc@ec2-23-23-228-115.compute-1.amazonaws.com:5432/d9crmiih79tddt')
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
conn = pg.connect(db)
# conn = pg.connect(user='postgres', password='postgres', host='192.168.1.98', database='wkt')  # dev port default 5432
'''
cursor = conn.cursor()
dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


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
		temp_dic = dict(zip(keys, row[1:]))
		m_dic[row[0]] = temp_dic
	return jsonify(m_dic)


def main_q_one(query):
	cursor.execute(query)
	results = cursor.fetchall()
	m_dic = {}
	for row in results:
		m_dic[row[0]] = row[1]
	return jsonify(m_dic)
