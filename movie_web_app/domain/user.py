from movie_web_app.domain.watchlist import WatchList


class User:
    def __init__(self, user_name: str, password: str):
        if user_name == "" or type(user_name) is not str:
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()

        if password == "" or type(password) is not str:
            self.__password = None
        else:
            self.__password = password.strip()

        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = 0
        self.__watchlist = WatchList()

    @property
    def user_name(self):
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

    @property
    def watchlist(self):
        return self.__watchlist

    def __repr__(self):
        return f"<User {self.__user_name}>"

    def __eq__(self, other):
        return self.__user_name == other.__user_name

    def __lt__(self, other):
        return self.__user_name < other.__user_name

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, watched_movie):
        if watched_movie not in self.__watched_movies:
            self.__watched_movies.append(watched_movie)
        self.__time_spent_watching_movies_minutes += watched_movie.runtime_minutes

    def add_review(self, new_review):
        self.__reviews.append(new_review)
        new_review.movie.update_ratings(new_review)

    def top_ten(self, movie_database):
        recommendations = []
        for i in range(10):
            recommendations.append(movie_database.dataset_of_movies[i])
        return recommendations

    def give_recommendation_actor(self, movie_database):
        watched = 0
        will_watch = 0
        preference_list = {}
        recommended_movies = {}
        lowest_movie = None
        lowest_score = None
        if len(self.__watched_movies) != 0:
            watched = 1
        if self.__watchlist.size() != 0:
            will_watch = 1
        if watched == 0 and will_watch == 0:
            return self.top_ten(movie_database)
        if watched == 1:
            for movie in self.__watched_movies:
                weighting = 1
                for review in self.__reviews:
                    if review.movie == movie:
                        weighting = review.rating - 5
                for actor in movie.actors:
                    if actor not in preference_list:
                        preference_list[actor] = weighting
                    else:
                        preference_list[actor] += weighting
        if will_watch == 1:
            for movie in self.__watchlist.watchlist:
                weighting = 1
                for actor in movie.actors:
                    if actor not in preference_list:
                        preference_list[actor] = weighting
                    else:
                        preference_list[actor] += weighting
        for movie in movie_database.dataset_of_movies:
            relation = 0
            if movie in self.__watched_movies or movie in self.__watchlist.watchlist:
                continue
            for actor in movie.actors:
                relation += preference_list.get(actor, 0)
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
        print(recommended_movies)
        print(preference_list)
        x = {key: value for key, value in sorted(recommended_movies.items(), key=lambda item: item[1])}
        top_ten_recommendations = list(x.keys())
        return top_ten_recommendations

    def give_recommendation_genre(self, movie_database):
        watched = 0
        will_watch = 0
        preference_list = {}
        recommended_movies = {}
        lowest_movie = None
        lowest_score = None
        if len(self.__watched_movies) != 0:
            watched = 1
        if self.__watchlist.size() != 0:
            will_watch = 1
        if watched == 0 and will_watch == 0:
            return self.top_ten(movie_database)
        if watched == 1:
            for movie in self.__watched_movies:
                weighting = 1
                for review in self.__reviews:
                    if review.movie == movie:
                        weighting = review.rating - 5
                for genre in movie.genres:
                    if genre not in preference_list:
                        preference_list[genre] = weighting
                    else:
                        preference_list[genre] += weighting
        if will_watch == 1:
            for movie in self.__watchlist.watchlist:
                weighting = 1
                for genre in movie.genres:
                    if genre not in preference_list:
                        preference_list[genre] = weighting
                    else:
                        preference_list[genre] += weighting
        for movie in movie_database.dataset_of_movies:
            relation = 0
            if movie in self.__watched_movies or movie in self.__watchlist.watchlist:
                continue
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
