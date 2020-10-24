from flask import Blueprint, request, render_template, redirect, url_for, session

import movie_web_app.datafilereaders.repository as repo
import movie_web_app.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_genres():
    return "<h>hello</h>"


def get_selected_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)
    return movies