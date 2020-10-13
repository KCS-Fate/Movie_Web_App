"""Flask configuration variables."""

from os import environ, path
import os
from dotenv import load_dotenv


# Load environment variables from file .env, stored in this directory.
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""

    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    #FLASK_ENV = environ.get('FLASK_ENV')