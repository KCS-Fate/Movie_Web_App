import csv
import os
from datetime import datetime
from typing import List

from werkzeug.security import generate_password_hash
from bisect import bisect_left, insort_left
from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domainmodel.model import User, Actor, Director, Genre, Movie, Review, WatchList, \
    make_actor_association, make_genre_association, make_director_association, make_review


class MemoryRepository(AbstractRepository):
    # Movies are ordered by title then by release year
    def __init__(self):
        self.__users = list()
        self.__actors = list()
        self.__directors = list()
        self.__genres = list()
        self.__movies = list()
        self.__reviews = list()
        self.__watchlists = list()
        self.__movie_index = dict()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username), None)

    def get_user_reviews(self, user: User) -> List[Review]:
        if user in self.__users:
            return user.reviews
        return None

    def add_actor(self, actor: Actor):
        if isinstance(actor, Actor):
            self.__actors.append(actor)

    def get_actor(self, actor_full_name) -> Actor:
        return next((actor for actor in self.__actors if actor.actor_full_name == actor_full_name), None)

    def add_director(self, director: Director):
        if isinstance(director, Director):
            self.__directors.append(director)

    def get_director(self, director_full_name) -> Director:
        return next((director for director in self.__directors if director.director_full_name == director_full_name),
                    None)

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre):
            self.__genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def add_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            # self._movies.append(movie)
            insort_left(self.__movies, movie)
            self.__movie_index[movie.id] = movie

    def get_movie(self, title: str, release_year: int):
        return next((movie for movie in self.__movies if (movie.title == title and movie.release_year == release_year)),
                    None)

    def get_movies_by_release_year(self, target_year:int):
        matching_movies = list()
        for movie in self.__movies:
            if movie.release_year == target_year:
                matching_movies.append(movie)
        return matching_movies

    def get_movies_by_actor(self, actor_fullname:str):
        actor_fullname = actor_fullname.strip()
        actor = next((actor for actor in self.__actors if actor.actor_full_name.lower() == actor_fullname.lower()), None)
        if actor is not None:
            played_movies = [movie for movie in actor.tagged_movies]
        else:
            played_movies = list()
        return played_movies

    def get_movies_by_director(self, director_fullname:str):
        director_fullname = director_fullname.strip()
        director = next((director for director in self.__directors if director.director_full_name.lower() == director_fullname.lower()), None)
        if director is not None:
            directed_movies = [movie for movie in director.tagged_movies]
        else:
            directed_movies = list()
        return directed_movies

    def search_movies_by_actor_and_director(self, actor_fullname: str, director_fullname: str):
        actor_fullname = actor_fullname.strip()
        director_fullname = director_fullname.strip()
        output = list()
        movies_played_by_actor = self.get_movies_by_actor(actor_fullname=actor_fullname)
        if len(movies_played_by_actor) > 0:
            output = [movie for movie in movies_played_by_actor if movie.director.director_full_name.lower() == director_fullname.lower()]
        return output

    def search_movie_by_title(self, title: str) -> List[Movie]:
        output = list()
        for current_movie in self.__movies:
            if title.lower() in current_movie.title.lower():
                output.append(current_movie)
        return output

    def get_number_of_movies(self):
        return len(self.__movies)

    def get_newest_movie(self):
        movie = None

        if len(self.__movies) > 0:
            self.__movies.sort(key=lambda x: x.release_year, reverse=True)
            movie = self.__movies[0]
        return movie

    def get_oldest_movie(self):
        movie = None
        if len(self.__movies) > 0:
            self.__movies.sort(key=lambda x: x.release_year, reverse=False)
            movie = self.__movies[0]
        return movie

    def get_release_year_of_previous_movie(self, movie:Movie):
        previous_year = None

        try:
            index = self.movie_index(movie)
            for stored_movie in reversed(self.__movies[0:index]):
                if stored_movie.release_year < movie.release_year:
                    previous_year = stored_movie.release_year
                    break
        except ValueError:
            pass

        return previous_year


    def get_release_year_of_next_movie(self, movie: Movie):
        next_year = None

        try:
            index = self.movie_index(movie)
            for stored_movie in self.__movies[index + 1:len(self.__movies)]:
                if stored_movie.release_year > movie.release_year:
                    next_year = stored_movie.release_year
                    break
        except ValueError:
            pass

        return next_year

    def get_movie_by_id(self, index: int):
        movie = None

        try:
            movie = self.__movie_index[index]
        except KeyError:
            pass
        return movie

    def get_movie_indexes_for_genre(self, genre_name: str):
        genre = next((genre for genre in self.__genres if genre.genre_full_name == genre_name), None)
        if genre is not None:
            movie_indexes = [movie.id for movie in genre.movie_genres]
        else:
            movie_indexes = list()
        return movie_indexes

    def get_movie_actors(self, movie: Movie) -> List[Actor]:
        if movie in self.__movies:
            return movie.actors
        return None

    def get_movie_release_year(self, movie: Movie) -> int:
        if movie in self.__movies:
            return movie.release_year
        return None

    def get_movie_description(self, movie: Movie) -> str:
        if movie in self.__movies:
            return movie.description
        return None

    def get_movie_director(self, movie: Movie) -> Director:
        if movie in self.__movies:
            return movie.director
        return None

    def get_movie_reviews(self, movie: Movie):
        if movie in self.__movies:
            return movie.reviews
        return None

    def get_movie_genres(self, movie: Movie) -> List[Genre]:
        if movie in self.__movies:
            return movie.genres
        return None

    def get_movie_runtime_minutes(self, movie: Movie) -> int:
        if movie in self.__movies:
            return movie.runtime_minutes
        return None

    def get_movies_by_id(self, index_list):
        # strip out any ids in the index_list that don't represent the Movie indexes in the repository
        existing_indexes = [index for index in index_list if index in self.__movie_index]
        movies = [self.__movie_index[index] for index in existing_indexes]
        return movies

    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self) -> List[Review]:
        return self.__reviews

    def get_total_number_of_reviews(self) -> int:
        return len(self.__reviews)

    def add_watchlist(self, watchlist: WatchList):
        self.__watchlists.append(watchlist)

    def get_watchlist(self) -> List[WatchList]:
        return self.__watchlists

    def movie_index(self, movie: Movie):
        index = bisect_left(self.__movies, movie)
        if index != len(self.__movies) and self.__movies[index].release_year == movie.release_year:
            return index
        raise ValueError

    def get_user_reviewed_movie(self, username:str):
        user = self.get_user(username)
        movies = list()
        if user is not None:
            for current_review in user.reviews:
                movies.append(current_review.movie)
        return movies

    def user_recommendations_by_genre(self, username: str) -> List[Movie]:
        user = self.get_user(username)
        preference_list = {}
        recommended_movies = {}
        reviewed = []
        lowest_movie = None
        lowest_score = None
        if not user.reviews:
            return self.__movies[0:10]
        for review in user.reviews:
            movie = review.movie
            reviewed.append(movie)
            weighting = review.rating - 5
            for genre in movie.genres:
                if genre not in preference_list:
                    preference_list[genre] = weighting
                else:
                    preference_list[genre] += weighting
        for movie in self.__movies:
            if movie in reviewed:
                continue
            relation = 0
            for genre in movie.genres:
                relation += preference_list.get(genre, 0)
            if len(recommended_movies) == 0:
                recommended_movies[movie] = relation
                lowest_movie = movie
                lowest_score = relation
            else:
                if len(recommended_movies) < 10:
                    recommended_movies[movie] = relation
                    if relation < lowest_score:
                        lowest_score = relation
                        lowest_movie = movie
                else:
                    if relation > lowest_score:
                        recommended_movies.pop(lowest_movie)
                        recommended_movies[movie] = relation
                        lowest_movie = min(recommended_movies.keys(), key=(lambda k: recommended_movies[k]))
                        lowest_score = recommended_movies[lowest_movie]
        x = {key: value for key, value in sorted(recommended_movies.items(), key=lambda item: item[1])}
        top_ten_recommendations = list(x.keys())
        return top_ten_recommendations


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies(data_path: str, repo: MemoryRepository):
    genres = dict()
    directors = dict()
    actors = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):
        movie = Movie(data_row[1], int(data_row[6]))
        movie.id = int(data_row[0])
        movie_genres = data_row[2].split(",")
        movie.description = data_row[3]
        movie.director = data_row[4]
        movie_actors = data_row[5].split(",")
        movie.runtime_minutes = int(data_row[7])
        movie.rating = float(data_row[8])
        movie.votes = int(data_row[9])
        revenue = data_row[10]
        metascore = data_row[11]

        for genre in movie_genres:
            if genre not in genres.keys():
                genres[genre] = list()
            genres[genre].append(movie.id)

        for actor in movie_actors:
            if actor not in actors.keys():
                actors[actor] = list()
            actors[actor].append(movie.id)

        if movie.director not in directors.keys():
            directors[movie.director] = list()
        directors[movie.director].append(movie.id)

        if revenue[0].isdigit():
            movie.revenue = float(revenue)
        else:
            movie.revenue = 'Not Available'

        if metascore[0].isdigit():
            movie.metascore = float(metascore)
        else:
            movie.metascore = 'Not Available'

        repo.add_movie(movie)

    for actor_name in actors.keys():
        actor = Actor(actor_name)
        for movie_id in actors[actor_name]:
            movie = repo.get_movie_by_id(movie_id)
            make_actor_association(movie, actor)
        repo.add_actor(actor)

    for genre_name in genres.keys():
        genre = Genre(genre_name)
        for movie_id in genres[genre_name]:
            movie = repo.get_movie_by_id(movie_id)
            make_genre_association(movie, genre)
        repo.add_genre(genre)

    for director_name in directors.keys():
        director = Director(director_name)
        for movie_id in directors[director_name]:
            movie = repo.get_movie_by_id(movie_id)
            make_director_association(movie, director)
        repo.add_director(director)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()
    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[int(data_row[0])] = user
    return users


def load_reviews(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        movie = repo.get_movie_by_id(int(data_row[2]))
        user = users[int(data_row[1])]
        review = make_review(review_text=data_row[3], user=user, movie=movie, rating=int(data_row[4]), timestamp=datetime.fromisoformat(data_row[5]))
        repo.add_review(review)


def populate(data_path: str, repo: MemoryRepository):
    # Load movies from Data1000Movies.csv
    load_movies(data_path, repo)

    # Load users into the repository
    users = load_users(data_path, repo)

    # Load reviews into the repository
    load_reviews(data_path, repo, users)
