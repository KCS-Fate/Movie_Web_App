import abc
from typing import List
from datetime import date

from movie_web_app.domain.methods import Movie, Actor, Genre, Director, Review, User


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.
        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a movie to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, id: int):
        """ Returns the Movie with id from the repository.
        If there is no movie with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the number of Movies in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, id_list):
        """ Returns a list of articles, whose ids match those in id_list from the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_genre(self, genre_name: str):
        """ Returns a list of ids representing Articles that are tagged by genre_name"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Get the first Movie in the repo. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Get the last Movie in the repo. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_actor(self, actor_name: str):
        """ Returns a list of ids representing Articles that are tagged by genre_name"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_director(self, director_name: str):
        """ Returns a list of ids representing Articles that are tagged by genre_name"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        """ Adds a actor to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self) -> List[Actor]:
        """ Returns the actors stored in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a genre to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self) -> List[Genre]:
        """ Returns the genres stored in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        """ Adds a actor to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self) -> List[Director]:
        """ Returns the actors stored in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Comment to the repository.
        If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Comment not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Comment not correctly attached to an Article')

    @abc.abstractmethod
    def get_reviews(self) -> List[Review]:
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError



