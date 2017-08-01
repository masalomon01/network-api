from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS

from config import config

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
