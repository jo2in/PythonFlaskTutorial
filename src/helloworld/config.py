import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEFAULT_SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'helloworld_app.db')


class Config(object):
        SECRET_KEY = os.getenv('SECRET_KEY', 'super_secret_key')
        SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', DEFAULT_SQLALCHEMY_DATABASE_URI)
        SQLALCHEMY_TRACK_MODIFICATIONS = False
