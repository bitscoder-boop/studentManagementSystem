import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///foo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
