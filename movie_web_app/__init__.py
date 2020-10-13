from flask import Flask
from markupsafe import escape
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader

import os
import sys


def create_app(test_config=None):

    app = Flask(__name__)
    app.config.from_object("config.Config")
    print(app.config)
    filename = 'datafiles/Data1000MoviesTest.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    data_path = os.path.join('movie_web_app', 'datafilereaders', 'datafiles')

    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

    return app
