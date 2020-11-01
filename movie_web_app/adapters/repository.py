import abc
from typing import List
from movie_web_app.domainmodel.model import User, Actor, Director, Genre, Movie, Review, WatchList

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        """ Adds an actor to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_full_name) -> Actor:
        """
        Returns an Actor with the full name of actor_full_name
        If there is no Actor with the given full name, this method returns None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        """ Adds a director to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_full_name) -> Director:
        """
        Returns a Director with the appropriate full_name.
        If no director in the repository is with the given fullname, this method returns None.
        """

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a genre to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the genres stored in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie:Movie):
        """ Adds a movie to the repository and add the index of movie to repo """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title: str, release_year: int):
        """
        Returns a Movie with the given title and release_year
        If no movie in the repository has the given title and release_year, this method
        returns None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_release_year(self, target_year: int) -> List[Movie]:
        """ Return a list of Movies tha were released in the target_year

            If there are no Movies on the given year, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, actor_fullname: str) -> List[Movie]:
        """
        Returns a list of movies played by the actor.
        Returns an empty list if the supplied actor does not exist or the actor hasn't played any movie
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, director_fullname: str) -> List[Movie]:
        """
        Returns a list of movies directed by the director
        Returns an empty list of the supplied directed does not exist or the director didn't direct any movie
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search_movie_by_title(self, title: str) -> List[Movie]:
        """
        Returns a list of movies that matches the title
        Returns an empty list if no matched movie title found
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_newest_movie(self):
        """
        Return the latest Movie, ordered by release year, from the repository.
        Returns None if the repository is empty
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_oldest_movie(self):
        """
        Return the oldest Movie, ordered by release year, from the repository
        Returns None if the repository is empty
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_release_year_of_previous_movie(self, movie: Movie):
        """
        Returns the release year of a Movie that immediately precedes movie.
        If movie is the first Movie in the repository, this method returns none because there are no Movies
        in the previous year.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_release_year_of_next_movie(self, movie: Movie):
        """
        Returns the release year of a Movie that immediately after movie.
        If movie is the first Movie in the repository, this method returns none because there are no Movies
        in the previous year.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the total number of movies in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_id(self, index: int):
        """
        Returns a Movie with the given index
        Returns None if the movie does not exist in the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, index_list):
        """
        Returns Movies with the given indexes
        Returns None if the movie does not exist in the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genre(self, genre_name: str):
        """
        Returns a list of movie indexes representing Movies that are classified by the given genre_name
        If there are no movie are classified by the given genre name then the method returns an empty list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """
        Adds a Review to the repository

        If the review doesn't have bidrectional links with a Movie and a User, this method raises a
        RepositoryException and doesn't update the repository
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException("Review not correctly attached to a User")
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException("Review not correctly attached to a Movie")

    @abc.abstractmethod
    def get_reviews(self) -> List[Review]:
        """ Returns reviews stored in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_watchlist(self, watchlist: WatchList):
        """ Adds an empty watchlist to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_watchlist(self) -> List[WatchList]:
        """ Returns a list of watchlist in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def user_recommendations_by_genre(self, username: str) -> List[Movie]:
        """ Returns a list of movies recommend for the user """
        raise NotImplementedError