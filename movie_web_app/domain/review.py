from datetime import datetime

from movie_web_app.domain.movie import Movie

class Review:
    def __init__(self, movie, review_text: str, rating: int):
        if type(movie) is not Movie:
            self.__movie = None
        else:
            self.__movie = movie

        if review_text == "" or type(review_text) is not str:
            self.__review_text = None
        else:
            self.__review_text = review_text

        if rating == "" or type(rating) is not int or rating > 10 or rating < 1:
            self.__rating = None
        else:
            self.__rating = rating

        self.__timestamp = datetime.now()

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return f"<Movie: {self.__movie}\nReview: {self.__review_text}\nRating: {self.__rating}\nWritten at: {self.__timestamp}>"

    def __eq__(self, other):
        return self.__movie == other.__movie and self.__review_text == other.__review_text and self.__rating == other.__rating