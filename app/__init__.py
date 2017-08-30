from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from config import config
import psycopg2 as pg
from urllib.parse import urlparse
import urllib.parse


db = SQLAlchemy()
cors = CORS()


def create_app(config_name):
	"""Factory for Flask App"""
	app = Flask("")
	# app = Flask("__name__")
	app.config.from_object(config[config_name])
	db.init_app(app)
	cors.init_app(app)

	# attach routes and custom error pages here
	from .main import main as main_blueprint
	from .api_1_0 import api as api_1_0_blueprint
	from .api_1_5 import api_bp as api_1_5_blueprint


	app.register_blueprint(main_blueprint)
	app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
	app.register_blueprint(api_1_5_blueprint, url_prefix='/api/v1.5')

	return app


def get_vars(CONFIG, var):
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


		if var == 'schema':
			return schema
		elif var == 'conn':
			return conn
		else:
			print('error that variable does not exist check app/init.py')

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

		if var == 'schema':
			return schema
		elif var == 'conn':
			return conn
		else:
			print('error that variable does not exist check app/init.py')

	elif CONFIG == 'developer' or  CONFIG == 'default':
		schema = 'developer'
		url = urlparse('postgres://dtolyqrislafqi:5a3d4791e40522df04870a9fb280348eac48e6bffb799095000b2305b61cbbbc@ec2-23-23-228-115.compute-1.amazonaws.com:5432/d9crmiih79tddt')
		db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
		conn = pg.connect(db)
		# conn = pg.connect(user='postgres', password='postgres', host='192.168.1.98', database='wkt')  # dev port default 5432

		if var == 'schema':
			return schema
		elif var == 'conn':
			return conn
		else:
			print('error that variable does not exist check app/init.py')

	else:
		print('there is an error on your CONFIG environment variable it should be production, sandbox or developer')