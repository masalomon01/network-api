import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Metropia Networkland'
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or \
    #                          'postgres://dtolyqrislafqi:5a3d4791e40522df04870a9fb280348eac48e6bffb799095000b2305b61cbbbc@ec2-23-23-228-115.compute-1.amazonaws.com:5432/d9crmiih79tddt'
    MONGO_DBNAME = "Traffic"

    @staticmethod
    def init_app(app):
        pass


class SandboxConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'postgres://dtolyqrislafqi:5a3d4791e40522df04870a9fb280348eac48e6bffb799095000b2305b61cbbbc@ec2-23-23-228-115.compute-1.amazonaws.com:5432/d9crmiih79tddt'

    SERVER_NAME = os.environ.get("SERVER_NAME")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'postgres://dtolyqrislafqi:5a3d4791e40522df04870a9fb280348eac48e6bffb799095000b2305b61cbbbc@ec2-23-23-228-115.compute-1.amazonaws.com:5432/d9crmiih79tddt'

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.environ.get("MONGO_URL") or "localhost"


class ProductionConfig(Config):
    SERVER_NAME = os.environ.get("SERVER_NAME")
    MONGO_URI = os.environ.get("MONGO_URL") or "localhost"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'sandbox': SandboxConfig,
    'default': DevelopmentConfig
}
