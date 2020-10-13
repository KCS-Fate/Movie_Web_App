from movie_web_app.domain.genre import Genre
from movie_web_app.domain.actor import Actor
from movie_web_app.domain.director import Director

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
        self.__title = None
        self.__description = None
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = None
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
        if type(movie_director) is not Director or movie_director.director_full_name == "":
            self.__director = None
        else:
            self.__director = movie_director
        return

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

    def __repr__(self):
        return f"<Movie {self.__movie_full_name}, {self.__movie_release_year}>"

    def __eq__(self, other):
        return self.__movie_full_name == other.__movie_full_name and self.__movie_release_year == other.__movie_release_year

    def __lt__(self, other):
        return (self.__movie_full_name, self.__movie_release_year) < (other.__movie_full_name, other.__movie_release_year)

    def __hash__(self):
        return hash(self.__movie_full_name + str(self.__movie_release_year))