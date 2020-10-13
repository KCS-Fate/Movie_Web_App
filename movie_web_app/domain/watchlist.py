from movie_web_app.domain.movie import Movie

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