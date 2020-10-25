from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields.html5 import SearchField, DecimalField
from password_validator import PasswordValidator

from functools import wraps

import movie_web_app.utilities.utilities as utilities
import movie_web_app.authentication.services as services
import movie_web_app.adapters.repository as repo
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange



# Configure Blueprint
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication'
)

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_not_unique = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # User the service layer to attempt to add the new user
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)

            # All is well, redirect the user to the login page.
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            username_not_unique = 'Your username is already taken - please try another'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'authentication/credentials.html',
        title='Register',
        form_login=form,
        form=SearchForm(),
        handler_url=url_for('movies_bp.search'),
        title_form=SearchByTitleForm(),
        handler_url_title=url_for('movies_bp.search_by_title'),
        username_error_message=username_not_unique,
        handler_url_login=url_for('authentication_bp.register'),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls()
    )

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_not_recognised = None
    password_does_not_match_username = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            user = services.get_user(form.username.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('movies_bp.suggest_movie'))

        except services.UnknownUserException:
            username_not_recognised = 'Username not recognised - please supply another'

        except services.AuthenticationException:
            password_does_not_match_username = 'Password does not match supplied username - please check and try again'

    return render_template(
        'authentication/credentials.html',
        title='Login',
        username_error_message=username_not_recognised,
        password_error_message=password_does_not_match_username,
        form_login=form,
        title_form=SearchByTitleForm(),
        form=SearchForm(),
        handler_url=url_for('movies_bp.search'),
        handler_url_title=url_for('movies_bp.search_by_title'),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls()
    )


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = 'Your password should have at least 8 characters, an upper case letter, lower case letter, and digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Your username is required'),
        Length(min=3, message='Your username is too short')])
    password = PasswordField('Password', [
        validators.DataRequired(message='Your password is required'),
        validators.EqualTo('confirm', message='Passwords must match'),
        PasswordValid()])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    confirm = None
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    actor = SearchField('Please enter actor fullname')
    director = SearchField('Please enter director fullname')
    search = SubmitField('Search')


class SearchByTitleForm(FlaskForm):
    title = SearchField('Please enter movie title')
    search = SubmitField('Search')