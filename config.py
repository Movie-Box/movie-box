import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENVIRONMENT = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Database
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'moviebox.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # FACEBOOK_ID = os.environ.get("FACEBOOK_OAUTH_CLIENT_ID")
    # FACEBOOK_SECRET = os.environ.get("FACEBOOK_OAUTH_CLIENT_SECRET")
    
    # GOOGLE_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    # GOOGLE_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")