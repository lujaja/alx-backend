#!/usr/bin/env python3
""" Mock logging in """
from flask import g, request, Flask, render_template
from flask_babel import Babel, gettext as _
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime

app = Flask(__name__)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """ Config class """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    BABEL_SUPPORTED_LOCALES = ['en', 'fr']


app.config.from_object(Config)

babel = Babel(app)


def get_user(login_as):
    """Get user"""
    if login_as is None or int(login_as) not in users.keys():
        return None
    return users.get(int(login_as))


@app.before_request
def before_request():
    """Before request"""
    id = request.args.get('login_as')
    user = get_user(id)
    if user:
        g.user = user
    else:
        g.user = None


@babel.localeselector
def get_locale():
    """"Get locale"""
    locale = request.args.get('locale')
    if locale and locale in app.config['BABEL_SUPPORTED_LOCALES']:
        return locale
    if g.user and g.user.get(
        'locale'
    ) in app.config['BABEL_SUPPORTED_LOCALES']:
        return g.user['locale']
    locale = request.accept_languages.best_match(
        app.config['BABEL_SUPPORTED_LOCALES']
    )
    if locale:
        return locale
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """Get timezone"""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except UnknownTimeZoneError:
            pass
    if g.user and g.user.get('timezone'):
        try:
            return pytz.timezone(g.user['timezone']).zone
        except UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Index"""
    user_timezone = get_timezone()
    current_time = datetime.now(pytz.timezone(user_timezone)).strftime('%c')

    return render_template(
        'index.html',
        locale=get_locale(),
        user=g.user,
        current_time=current_time
    )


if __name__ == '__main__':
    """Main Function"""
    app.run(host='0.0.0.0', port=5000, debug=True)
