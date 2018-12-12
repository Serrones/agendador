import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You shall not pass'

    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')

    # SQLALCHEMY_DATABASE_LOG = 'sqlite:///' + os.path.join(basedir, 'log.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
