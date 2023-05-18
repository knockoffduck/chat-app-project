import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

    # SQLALCHEMY_DATABASE_URI = os.getenv(
    #         'TEST_DATABASE_URI', default=f"sqlite:///{os.path.join(basedir), 'tests/test.db'}")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'tests', 'test.db')

    