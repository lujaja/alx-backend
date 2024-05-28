#!/usr/bin/env python3
"""  User locale"""
from flask import g, request, Flask, render_template
from flask_babel import Babel, gettext as _
import pytz
from pytz.exceptions import UnknownTimeZoneError

app = Flask(__name__)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    BABEL_SUPPORTED_LOCALES = ['en', 'fr']


app.config.from_object(Config)

babel = Babel(app)


def get_user(login_as):
    if login_as is None or int(login_as) not in users.keys():
        return None
    return users.get(int(login_as))


@app.before_request
def before_request():
    id = request.args.get('login_as')
    user = get_user(id)
    if user is not None:
        print(user)
        g.user = user
    else:
        g.user = None


@babel.localeselector
def get_locale():
    """Get locale"""
    if g.user:
        locale = g.user.get('locale')
        if locale in app.config['BABEL_SUPPORTED_LOCALES']:
            return locale
    locale = request.args.get('locale')
    if locale in app.config['BABEL_SUPPORTED_LOCALES']:
        return locale
    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Index"""
    return render_template(
        '6-index.html',
        locale=get_locale()
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
