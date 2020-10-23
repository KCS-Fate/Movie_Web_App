from typing import Iterable
import random

from movie_web_app.datafilereaders.repository import AbstractRepository
from movie_web_app.domain.methods import Movie


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genre()
    genre_names = [genre.genre_full_name for genre in genres]

    return genre_names

def get_actor_names(repo: AbstractRepository):
    actors = repo.get_actor()
    actor_names = [actor.actor_full_name for actor in actors]

    return actor_names

def get_director_name(repo: AbstractRepository):
    directors = repo.get_director()
    director_names = [director.director_full_name for director in directors]

    return director_names


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = movie_count - 1

    # Pick distinct and random articles.
    random_ids = random.sample(range(1, movie_count), quantity)
    articles = repo.get_movies_by_id(random_ids)

    return articles_to_dict(articles)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'date': movie.date,
        'title': movie.title,
        'rating': movie.rating
    }
    return movie_dict


def articles_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
