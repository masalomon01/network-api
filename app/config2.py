import os
import psycopg2 as pg
from urllib.parse import urlparse
import urllib.parse


def get_vars(CONFIG):
	# config can only be default(development), development, sandbox, production
	if CONFIG == 'production':
		schema = 'production'
		urllib.parse.uses_netloc.append("postgres")
		url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
		conn = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)
		cursor = conn.cursor()

		return schema, conn, cursor

	elif CONFIG == 'sandbox':
		schema = 'sandbox'
		urllib.parse.uses_netloc.append("postgres")
		url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
		conn = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)
		cursor = conn.cursor()

		return schema, conn, cursor

	else:
		schema = 'developer'
		url = urlparse('postgres://dtolyqrislafqi:5a3d4791e40522df04870a9fb280348eac48e6bffb799095000b2305b61cbbbc@ec2-23-23-228-115.compute-1.amazonaws.com:5432/d9crmiih79tddt')
		db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
		conn = pg.connect(db)
		# conn = pg.connect(user='postgres', password='postgres', host='192.168.1.98', database='wkt')  # dev port default 5432
		cursor = conn.cursor()

		return schema, conn, cursor