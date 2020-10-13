from movie_web_app.domain.methods import Movie, Actor, Genre, Director, Review, User, WatchList
import csv
from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from movie_web_app.datafilereaders.repository import AbstractRepository, RepositoryException


class MovieFileCSVReader(AbstractRepository):

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies = []
        self.__dataset_of_movies_index = dict()
        self.__dataset_of_actors = []
        self.__dataset_of_directors = []
        self.__dataset_of_genres = []

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    def get_movie(self, movie_name):
        if movie_name in self.__dataset_of_movies:
            x = self.__dataset_of_movies.index(movie_name)
            return self.__dataset_of_movies[x]
        return

    def load_users(self, data_path: str, repo: MovieFileCSVReader):
        for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
            users = dict()

            for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
                user = User(
                    username=data_row[1],
                    password=generate_password_hash(data_row[2])
                )
                repo.add_user(user)
                users[data_row[0]] = user
            return users

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            for row in movie_file_reader:
                if index == 0:
                    index += 1

                movie = Movie(row['Title'].strip(), int(row['Year'].strip()))
                genres = [Genre(x.strip()) for x in row['Genre'].split(',')]
                actors = [Actor(x.strip()) for x in row['Actors'].split(',')]
                director = Director(row['Director'].strip())
                movie.description = row['Description'].strip()
                movie.runtime_minutes = int(row['Runtime (Minutes)'].strip())
                movie.rating = float(row['Rating'].strip())
                movie.votes = int(row['Votes'].strip())
                revenue = row['Revenue (Millions)'].strip()
                metascore = row['Metascore'].strip()

                if revenue[0].isdigit():
                    movie.revenue = float(revenue)
                else:
                    movie.revenue = 'Not Available'

                if metascore[0].isdigit():
                    movie.metascore = float(metascore)
                else:
                    movie.metascore = 'Not Available'

                if movie not in self.__dataset_of_movies:
                    self.__dataset_of_movies.append(movie)

                for genre in genres:
                    if genre not in self.__dataset_of_genres:
                        self.__dataset_of_genres.append(genre)
                    movie.add_genre(genre)

                if director not in self.__dataset_of_directors:
                    self.__dataset_of_directors.append(director)
                movie.director = director

                for actor in actors:
                    if actor not in self.__dataset_of_actors:
                        self.__dataset_of_actors.append(actor)
                    movie.add_actor(actor)

                index += 1

    def populate(data_path: str, repo: MovieFileCSVReader()):
        pass

