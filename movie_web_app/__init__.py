from flask import Flask

import movie_web_app.datafilereaders.repository as repo
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader, populate

import os


def create_app(test_config=None):

    app = Flask(__name__)
    app.config.from_object("config.Config")
    data_path = os.path.join('movie_web_app', 'datafilereaders', 'datafiles')

    repo.repo_instance = MovieFileCSVReader()
    populate(data_path, repo.repo_instance)

    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

    return app
