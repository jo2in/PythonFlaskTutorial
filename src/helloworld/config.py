import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEFAULT_SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'helloworld_app.db')


class Config(object):
        SECRET_KEY = os.getenv('SECRET_KEY', 'super_secret_key')
        SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', DEFAULT_SQLALCHEMY_DATABASE_URI)
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        MAIL_SERVER = os.environ.get('MAIL_SERVER')
        MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
        MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        ADMINS = ['no-reply@example.com']
