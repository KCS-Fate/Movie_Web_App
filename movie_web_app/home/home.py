from flask import Blueprint, render_template
import movie_web_app.adapters.repository as repo
import movie_web_app.utilities.utilities as utilities
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from movie_web_app.movies.movies import SearchForm, SearchByTitleForm
from movie_web_app.movies.services import get_movies_by_id, get_random_movies
home_blueprint = Blueprint(
    'home_bp', __name__
)

@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    random_set = get_random_movies(repo=repo.repo_instance)

    for movie in random_set:
        movie['view_review_url'] = url_for('home_bp.home')
        movie['add_review_url'] = url_for('movies_bp.review_movie', movie=movie['id'])

    return render_template(
        'home/home.html',
        selected_movies=utilities.get_selected_movies(),
        movie_set=random_set,
        genre_urls=utilities.get_genres_and_urls(),
        form=SearchForm(),
        handler_url=url_for("movies_bp.search"),
        title_form = SearchByTitleForm(),
        handler_url_title = url_for('movies_bp.search_by_title')
    )

