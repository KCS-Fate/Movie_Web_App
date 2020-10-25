import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984', 'confirm': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(
    ('username', 'password', 'confirm', 'message'),(
        ('test', '', '', b'Your password is required'),
        ('test', 'test', '', b'Your password should have at least 8 characters, an upper case letter, lower case letter, and digit'),
        ('fmercury', 'Test#6^0', 'Test#6^0', b'Your username is already taken - please try another'),
    ))
def test_register_with_invalid_input(client, username, password, confirm, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password, 'confirm': confirm}
    )
    print('\n\n\n\n\n\n\n', response,'\n\n\n\n\n')
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage
    response = auth.login()
    assert response.headers['Location'] == "http://localhost/suggest"

    # Check that a session has been created for the logged-in user
    with client:
        client.get('/')
        assert session['username'] == 'thorke'


def test_logout(client, auth):
    # Login a user
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200


def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page
    response = client.get('/review?movie=1')
    response = client.post(
        '/review',
        data={'review': 'what a great movie!', 'movie_id': 1, 'rating': 10}
    )
    assert response.headers['Location'] == 'http://localhost/sidebar_movies_by_title?title=Guardians+of+the+Galaxy'


@pytest.mark.parametrize(('review', 'rating', 'messages'), (
        ('Fucking trash acting','3', (b'Your review must not contain profanity')),
        ('Hey', '5', (b'Your review is too short')),
        ('ass', '1', (b'Your review is too short', b'Your review must not contain profanity')),
))

def test_review_with_invalid_input(client, auth, review, rating, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article
    response = client.post(
        '/review',
        data={'review': review, 'movie_id': 1}
    )

    # Check that supplying invalid review text or not leaving a rating generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_movie_without_date(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_release_year')
    assert response.status_code == 200

    # Check that without providing a year query parameter the page includes the first movie
    assert b'Split' in response.data
    assert b'Sing' in response.data


def test_movies_with_date(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_release_year?year=2014')
    assert response.status_code == 200

    assert b'Guardians of the Galaxy' in response.data
    assert b'Prisoners' not in response.data


def test_movies_with_review(client):
    # Check that we can retrieve the movies page:
    response = client.get('/movies_by_release_year?year=2014&view_reviews_for=1')
    assert response.status_code == 200

    # Check that all comments for specified movie are included on the page
    assert b'Wonderful movie' in response.data
    assert b'Loved the plot, actors did a splendid job' in response.data
    assert b'Came to watch with my kids, they really enjoyed it!' in response.data


def test_movies_with_genre(client):
    # Check that we can retrieve the movie page
    response = client.get('/movies_by_genre?genre=Horror')
    assert response.status_code == 200

    # Check that all movies tagged as 'Horror' are returned back
    assert b'Split' in response.data
    assert b"Guardians of the Galaxy" not in response.data


def test_search_by_actor_fullname(client):
    # Check that we can search the movie page
    response = client.post('/sidebar', data={'actor': "Chris Pratt"})
    assert response.headers['Location'] == "http://localhost/search_movies_by_actor_or_director?actor=Chris+Pratt&director="

    # Check that we have the desired results returned by the search
    response = client.get('/search_movies_by_actor_or_director?actor=Chris+Pratt&director=')
    assert response.status_code == 200
    assert b'Guardians of the Galaxy' in response.data


def test_search_by_director_fullname(client):
    # Check that we can search the movie page
    response = client.post('/sidebar', data={'director': 'David Ayer'})
    assert response.headers['Location'] == 'http://localhost/search_movies_by_actor_or_director?actor=&director=David+Ayer'

    response = client.get('/search_movies_by_actor_or_director?actor=&director=David+Ayer')
    assert response.status_code == 200
    assert b'Suicide Squad' in response.data


def test_search_by_movie_title(client):
    # Check that we can search the movie page
    response = client.post('/search_by_title', data={'title': "Passengers"})
    assert response.headers['Location'] == 'http://localhost/sidebar_movies_by_title?title=Passengers'

    # Check that we can have the desired movie returned by the search
    response = client.get('/sidebar_movies_by_title?title=Passengers')
    assert response.status_code == 200
    assert b'Passengers' in response.data
    assert b'2016' in response.data

def test_can_suggest_movies_to_a_logged_in_user(client, auth):
    # Login a user
    auth.login()

    # Check that we can retrieve suggestions for the logged in user:
    response = client.get('/suggest')
    assert response.status_code == 200

    # Check that a desired movie is returned
    assert b'Rogue One' in response.data
