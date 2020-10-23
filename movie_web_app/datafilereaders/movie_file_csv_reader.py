import csv
import os
from typing import List
from bisect import insort_left

from werkzeug.security import generate_password_hash

from movie_web_app.datafilereaders.repository import AbstractRepository, RepositoryException
from movie_web_app.domain.methods import Movie, Genre, Director, User, Actor, Review, make_review, \
    make_actor_association, make_genre_association, make_director_association


class MovieFileCSVReader(AbstractRepository):

    def __init__(self):
        self.__movies = list()
        self.__movies_index = dict()
        self.__genres = list()
        self.__directors = list()
        self.__actors = list()
        self.__reviews = list()
        self.__users = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.users if user.username == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self.__movies, movie)
        self.__movies_index[movie.id] = movie

    def get_movie(self, id: int):
        movie = None

        try:
            movie = self.__movies_index[id]
        except KeyError:
            pass
        return movie

    def get_number_of_movies(self):
        return len(self.__movies)

    def get_movies_by_id(self, id_list):
        existing_ids = [id for id in id_list if id in self.__movies_index]
        movies = [self.__movies_index[id] for id in existing_ids]
        return movies

    def get_movie_ids_for_genre(self, genre_name: str):
        genre = next((genre for genre in self.__genres if genre.genre_full_name == genre_name), None)

        if genre is not None:
            movie_ids = [movie.id for movie in genre.movie_genres]
        else:
            # No Tag with name tag_name, so return an empty list.
            movie_ids = list()

        return movie_ids

    def add_genre(self, genre: Genre):
        self.__genres.append(genre)

    def get_genre(self) -> List[Genre]:
        return self.__genres

    def add_director(self, director: Director):
        self.__directors.append(director)

    def get_director(self) -> List[Director]:
        return self.__directors

    def add_actor(self, actor: Actor):
        self.__actors.append(actor)

    def get_actor(self) -> List[Actor]:
        return self.__actors

    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self) -> List[Review]:
        return self.__reviews


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


def load_users(data_path: str, repo: MovieFileCSVReader):
    users = dict()
    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        username=data_row[1]
        password=generate_password_hash(data_row[2])
        user = User(username, password)
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_movies(data_path: str, repo: MovieFileCSVReader):
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
            movie = repo.get_movie(movie_id)
            make_actor_association(movie, actor)
        repo.add_actor(actor)

    for genre_name in genres.keys():
        genre = Genre(genre_name)
        for movie_id in genres[genre_name]:
            movie = repo.get_movie(movie_id)
            make_genre_association(movie, genre)
        repo.add_genre(genre)

    for director_name in directors.keys():
        director = Director(director_name)
        for movie_id in directors[director_name]:
            movie = repo.get_movie(movie_id)
            make_director_association(movie, director)
        repo.add_director(director)


def load_reviews(data_path: str, repo: MovieFileCSVReader, users):
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        review = make_review(
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
            review_text=data_row[3],
            rating=float(data_row[4])
        )


def populate(data_path: str, repo: MovieFileCSVReader):
    # Load movies and information into the repository.
    load_movies(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_reviews(data_path, repo, users)



'''
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

'''
