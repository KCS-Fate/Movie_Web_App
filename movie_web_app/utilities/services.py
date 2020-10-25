from typing import Iterable, List
import random

from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domainmodel.model import Movie


def get_genre_names(repo:AbstractRepository) -> List[str]:
    genres = repo.get_genres()
    genre_names = [genre.genre_full_name for genre in genres]

    return genre_names


def get_random_movies(quantity, repo:AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of movie ids to generate if the repository has an insufficient number of movies
        quantity = movie_count - 1

    # Pick distinct and random movie
    random_ids = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)


def movie_to_dict(movie: Movie):
    movie_dict = {
        "title": movie.title,
        "release_year": movie.release_year,
        "actors": movie.actors,
        "director": movie.director
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]