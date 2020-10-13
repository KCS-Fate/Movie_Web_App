class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_full_name = None
        else:
            self.__genre_full_name = genre_name.strip()

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