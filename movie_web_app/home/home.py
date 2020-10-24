from flask import Blueprint, render_template, session

import movie_web_app.utilities.utilities as utilities


home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        title='Movie Home',
        username=session.get('username', 'visitor'),
        error_msg=None
    )