from datetime import date

from movie_web_app.domainmodel.model import User, Movie, Genre, make_review, make_genre_association, Review, \
    Actor, Director, ModelException

import pytest


@pytest.fixture()
def movie():
    movie = Movie('Moana', 2016)
    movie.id = int(14)
    movie_genres = "Animation,Adventure,Comedy".split(",")
    movie.description = "A terrible curse incurred by the demigod Maui ignites a young girls destiny"
    movie.director = 'Ron Clements'
    movie_actors = "Auli'i Cravalho, Dwayne Johnson, Rachel House, Temuera Morrison".split(",")
    movie.runtime_minutes = 107
    movie.rating = float(7.7)
    movie.votes = 118151
    revenue = 248.75
    metascore = 81


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def genre():
    return Genre('NewGenre')


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.comments:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie):
    assert movie.id == 14
    assert movie.release_year == 2016
    assert movie.title == 'Moana'
    assert movie.runtime_minutes == 107
    assert movie.rating == 7.7
    assert movie.votes == 118151
    assert movie.revenue == 248.75
    assert movie.metascore == 81
    assert movie.actors == "[<Actor Auli'i Cravalho>, <Actor Dwayne Johnson>, <Actor Rachel House>, <Actor Temuera Morrison>]"
    assert movie.genres == "[<Genre Animation>, <Genre Adventure>, <Genre Comedy>]"
    assert movie.director == "<Director Ron Clements>"

    assert repr(
        movie) == '<Movie Moana, 2016>'


def test_article_less_than_operator():
    article_1 = Movie('No Game No Life', 2014)

    article_2 = Movie('No Game No Life: 2', 2021)

    assert article_1 < article_2


def test_genre_construction(genre):
    assert genre.genre_full_name == 'NewGenre'

    for movie in genre.tagged_movies:
        assert False

    assert not genre.is_applied_to(Movie('TESTER', 2020))


def test_make_comment_establishes_relationships(movie, user):
    comment_text = 'What a great movie!'
    comment = make_review(comment_text, user, movie)

    # Check that the User object knows about the Comment.
    assert comment in user.reviews

    # Check that the Comment knows about the User.
    assert comment.user is user

    # Check that Article knows about the Comment.
    assert comment in movie.reviews

    # Check that the Comment knows about the Article.
    assert comment.movie is movie


def test_make_genre_associations(movie, genre):
    make_genre_association(movie, genre)

    # Check that the Article knows about the Tag.
    assert movie.is_tagged()
    assert movie.is_tagged_by(genre)

    # check that the Tag knows about the Article.
    assert genre.is_applied_to(movie)
    assert movie in genre.tagged_movies


def test_make_genre_associations_with_article_already_tagged(movie, genre):
    make_genre_association(movie, genre)

    with pytest.raises(ModelException):
        make_genre_association(movie, genre)

