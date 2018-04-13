import os


class Config(object):
        SECRET_KEY = os.getenv('SECRET_KEY', 'super_secret_key')
