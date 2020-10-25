from datetime import datetime
from typing import List
class Movie:
    def __init__(self, movie_full_name: str, movie_release_year: int):
        if movie_full_name == "" or type(movie_full_name) is not str:
            self.__movie_full_name = None
        else:
            self.__movie_full_name = movie_full_name.strip()

        if movie_release_year == "" or type(movie_release_year) is not int or movie_release_year < 1900:
            self.__movie_release_year = None
        else:
            self.__movie_release_year = movie_release_year
        self.__id: int = None
        self.__title: str = None
        self.__description: str = ""
        self.__director: Director = None
        self.__actors: List[Actor] = list()
        self.__genres: List[Genre] = list()
        self.__reviews: List[Review] = list()
        self.__runtime_minutes: int = 0
        self.__rating = 0
        self.__votes = 0
        self.__revenue = 'Not Available'
        self.__metascore = 'Not Available'

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, movie_title: str):
        if movie_title == "" or type(movie_title) is not str:
            self.__title = None
        else:
            self.__title = movie_title.strip()
        return

    @property
    def reviews(self) -> list():
        return iter(self.__reviews)

    @property
    def title(self):
        return self.__movie_full_name

    @property
    def release_year(self):
        return self.__movie_release_year

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        self.__id = id

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, movie_description: str):
        if movie_description == "" or type(movie_description) is not str:
            self.__description = None
        else:
            self.__description = movie_description.strip()
        return

    @property
    def director(self):
        return self.__director

    @director.setter
    def director(self, movie_director):
        self.__director = movie_director

    @property
    def actors(self):
        return self.__actors

    @property
    def genres(self):
        return self.__genres

    @property
    def runtime_minutes(self):
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, minutes: int):
        if minutes < 0 or type(minutes) is not int:
            raise ValueError
        else:
            self.__runtime_minutes = minutes
        return

    @property
    def rating(self):
        return round(self.__rating, 1)

    @rating.setter
    def rating(self, movie_rating: float):
        self.__rating = movie_rating

    @property
    def votes(self):
        return self.__votes

    @votes.setter
    def votes(self, total_votes: int):
        self.__votes = total_votes

    @property
    def revenue(self):
        return self.__revenue

    @revenue.setter
    def revenue(self, total_revenue):
        if type(total_revenue) is float:
            self.__revenue = total_revenue
        else:
            self.__revenue == 'Not Available'

    @property
    def metascore(self):
        return self.__metascore

    @metascore.setter
    def metascore(self, current_metascore: float):
        if type(current_metascore) is float:
            self.__metascore = current_metascore
        else:
            self.__metascore == 'Not Available'

    def add_genre(self, genre):
        if type(genre) is not Genre or genre.genre_full_name == "":
            return
        else:
            self.__genres.append(genre)
        return

    def remove_genre(self, genre_name):
        if genre_name in self.__genres:
            self.__genres.remove(genre_name)
        return

    def add_actor(self, actor):
        if type(actor) is not Actor or actor.actor_full_name == "":
            return
        else:
            self.__actors.append(actor)
        return

    def remove_actor(self, actor_name):
        if actor_name in self.__actors:
            self.__actors.remove(actor_name)
        return

    def update_ratings(self, review):
        self.__rating = ((self.__rating * self.__votes) + review.rating) / (self.__votes + 1)
        self.__votes += 1

    def add_review(self, review):
        self.__reviews.append(review)

    def __repr__(self):
        return f"<Movie {self.__movie_full_name}, {self.__movie_release_year}>"

    def __eq__(self, other):
        return self.__movie_full_name == other.__movie_full_name and self.__movie_release_year == other.__movie_release_year

    def __lt__(self, other):
        return (self.__movie_full_name, self.__movie_release_year) < (other.__movie_full_name, other.__movie_release_year)

    def __hash__(self):
        return hash(self.__movie_full_name + str(self.__movie_release_year))


class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.__actor_colleague = list()
        self.__movie_actors = list()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @property
    def actor_colleague(self):
        return iter(self.__actor_colleague)

    @property
    def tagged_movies(self):
        return iter(self.__movie_actors)

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self.__movie_actors

    def add_movie(self, movie: Movie):
        self.__movie_actors.append(movie)

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other):
        return other.__actor_full_name > self.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        if not self.check_if_this_actor_worked_with(colleague):
            self.__actor_colleagues.append(colleague)
        return

    def check_if_this_actor_worked_with(self, colleague):
        if colleague in self.__actor_colleagues:
            return True
        else:
            return False


class Director:
    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()
        self.__movies_directed = list()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    @property
    def tagged_movies(self):
        return iter(self.__movies_directed)

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        return self.__director_full_name == other.__director_full_name

    def __lt__(self, other):
        return other.__director_full_name > self.__director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)

    def add_movie(self, movie: Movie):
        self.__movies_directed.append(movie)

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self.__movies_directed


class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_full_name = None
        else:
            self.__genre_full_name = genre_name.strip()
        self.__movie_genres: List[Movie] = list()

    @property
    def movie_genres(self):
        return iter(self.__movie_genres)

    @property
    def number_of_unique_movies(self):
        return len(self.__movie_genres)

    @property
    def genre_full_name(self) -> str:
        return self.__genre_full_name

    def __repr__(self):
        return f"<Genre {self.__genre_full_name}>"

    def __eq__(self, other):
        return self.__genre_full_name == other.__genre_full_name

    def __lt__(self, other):
        return other.__genre_full_name > self.__genre_full_name

    def __hash__(self):
        return hash(self.__genre_full_name)

    def add_movie(self, movie: Movie):
        self.__movie_genres.append(movie)

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self.__movie_genres


class User:
    def __init__(self, user_name: str, password: str):
        self.__user_name = user_name
        self.__password = password
        self.__watched_movies = list()
        self.__reviews = list()
        self.__time_spent_watching_movies_minutes = 0

    @property
    def username(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    def __repr__(self):
        return "<User {}>".format(self.username)

    def __eq__(self, other):
        if self.username is None and other.username is None:
            return False
        return self.username == other.username

    def __lt__(self, other):
        return self.username < other.username

    def __hash__(self):
        return hash((self.__user_name, self.__password))

    def watch_movie(self, movie: Movie):
        if movie not in self.__watched_movies:
            self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        if review not in self.__reviews:
            self.__reviews.append(review)


class Review:
    def __init__(self, user: User, movie: Movie, review_text: str, rating: int, timestamp: datetime):
        self.__author = user
        self.__movie = movie
        self.__review_text = review_text
        self.__rating = None
        self.__timestamp = timestamp
        if type(rating) is int:
            self.__rating = rating

    @property
    def user(self) -> User:
        return self.__author

    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return "<Review {}, {}>".format(self.movie, self.timestamp)

    def __eq__(self, other):
        if self.movie == other.movie and self.review_text == other.review_text \
                and self.rating == other.rating and self.timestamp == other.timestamp:
            return True
        return False

    def hash(self):
        return hash((self.movie, self.timestamp))


class WatchList:
    def __init__(self):
        self.__watchlist = []

    @property
    def watchlist(self):
        return self.__watchlist

    def add_movie(self, movie):
        if type(movie) is Movie and movie not in self.__watchlist:
            self.__watchlist.append(movie)

    def remove_movie(self, movie):
        if type(movie) is Movie and movie in self.__watchlist:
            self.__watchlist.remove(movie)

    def first_movie_in_watchlist(self):
        return self.__watchlist[0]

    def select_movie_to_watch(self, index):
        if index < len(self.__watchlist):
            return self.__watchlist[index]
        else:
            return None

    def size(self):
        return len(self.__watchlist)

    def __iter__(self):
        self.pos = 0
        return self

    def __next__(self):
        if self.pos >= self.size():
            raise StopIteration
        else:
            self.pos += 1
            return self.__watchlist[self.pos - 1]


class ModelException(Exception):
    pass


def make_review(review_text: str, user: User, movie: Movie, rating: int, timestamp: datetime = datetime.today()):
    review = Review(user, movie, review_text, rating, timestamp)
    user.add_review(review)
    movie.add_review(review)
    return review


def make_actor_association(movie: Movie, actor: Actor):
    if actor.is_applied_to(movie):
        raise ModelException(f'Actor {actor.actor_full_name} already applied to Article "{movie.title}"')

    movie.add_actor(actor)
    actor.add_movie(movie)


def make_genre_association(movie: Movie, genre: Genre):
    if genre.is_applied_to(movie):
        raise ModelException(f'Genre {genre.genre_full_name} already applied to Article "{movie.title}"')

    movie.add_genre(genre)
    genre.add_movie(movie)

def make_director_association(movie: Movie, director: Director):
    if director.is_applied_to(movie):
        raise ModelException(f'director {director} already applied to Article "{movie.title}"')

    movie.director = director.director_full_name
    director.add_movie(movie)
