import random
from typing import List, Iterable
from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domainmodel.model import Movie, Review, Genre, make_review, Actor, Director


class NonExistentException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(review_text: str, username: str, movie_id: int, rating: int, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie_by_id(movie_id)
    if movie is None:
        raise NonExistentException

    # Check that the user exists
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create review
    review = make_review(review_text=review_text, user=user, movie=movie, rating=rating)

    # Update the repository
    repo.add_review(review)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie_by_id(movie_id)

    if movie is None:
        raise NonExistentException

    return movie_to_dict(movie)


def get_newest_movie(repo: AbstractRepository):
    movie = repo.get_newest_movie()

    return movie_to_dict(movie)


def get_oldest_movie(repo: AbstractRepository):
    movie = repo.get_oldest_movie()
    return movie_to_dict(movie)


def get_movies_by_release_year(year, repo: AbstractRepository):
    movies = repo.get_movies_by_release_year(target_year=year)

    prev_year = next_year = None
    if len(movies) > 0:
        prev_year = repo.get_release_year_of_previous_movie(movies[0])
        next_year = repo.get_release_year_of_next_movie(movies[0])

        # Convert Movies to dictionary form.
        movies = movies_to_dict(movies)

    return movies, prev_year, next_year


def get_movie_ids_for_genre(genre_name: str, repo: AbstractRepository):
    movie_ids = repo.get_movie_indexes_for_genre(genre_name)

    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert Movies to dictionary form
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie_by_id(movie_id)

    if movie is None:
        raise NonExistentException

    return reviews_to_dict(movie.reviews)


def search_movie_by_actor_fullname(actor_fullname: str, repo: AbstractRepository):

    movies = repo.get_movies_by_actor(actor_fullname=actor_fullname)
    if len(movies) == 0:
        raise NonExistentException

    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def search_movie_directed_by_director_fullname(director_fullname: str, repo: AbstractRepository):
    movies = repo.get_movies_by_director(director_fullname=director_fullname)
    if len(movies) == 0:
        raise NonExistentException
    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def search_movie_by_actor_and_director(actor_fullname: str, director_fullname: str, repo: AbstractRepository):
    movies = repo.search_movies_by_actor_and_director(actor_fullname=actor_fullname,
                                                      director_fullname=director_fullname)
    if len(movies) == 0:
        raise NonExistentException

    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def search_movie_by_title(title:str, repo:AbstractRepository):
    movies = repo.search_movie_by_title(title)
    if len(movies) == 0:
        raise NonExistentException

    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def get_random_movies(repo:AbstractRepository):
    movie_count = repo.get_number_of_movies()
    quantity = 5
    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = movie_count - 1

    # Pick distinct and random articles.
    random_ids = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)


def user_recommendations_by_genre(username: str, repo: AbstractRepository):
    movies = repo.user_recommendations_by_genre(username)
    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict

# ============================================
# Functions to convert model entities to dicts
# ============================================


def movie_to_dict(movie: Movie):
    movie_dict = {
        'id': movie.id,
        'title': movie.title,
        'release_year': movie.release_year,
        'description': movie.description,
        'director': movie.director,
        'actors': actors_to_dict(movie.actors),
        'genres': genres_to_dict(movie.genres),
        'runtime_minutes': movie.runtime_minutes,
        'reviews': reviews_to_dict(movie.reviews),
        'ratings': movie.rating,
        'revenue': movie.revenue
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def actor_to_dict(actor: Actor):
    actor_dict = {
        'actor_fullname': actor.actor_full_name
    }
    return actor_dict


def actors_to_dict(actors: Iterable[Actor]):
    return [actor_to_dict(actor) for actor in actors]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'genre_name': genre.genre_full_name,
        'number_of_classified_movies': genre.number_of_unique_movies,
        'classified_movies': [movie.id for movie in genre.movie_genres]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


def review_to_dict(review: Review):
    review_dict = {
        'username': review.user.username,
        'movie_id': review.movie.id,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


# ============================================
# Functions to convert dicts to model entities
# ============================================


def dict_to_movie(dict):
    movie = Movie(dict['title'], dict['release_year'])
    return movie
