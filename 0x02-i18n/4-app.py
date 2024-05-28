#!/usr/bin/env python3
""" Force locale with URL parameter """
from flask import g, request, Flask, render_template
from flask_babel import Babel, gettext as _

app = Flask(__name__)


class Config:
    """Config class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    BABEL_SUPPORTED_LOCALES = ['en', 'fr']


app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale():
    """Get locale"""
    locale = request.args.get('locale') or 'en'
    if locale in app.config['BABEL_SUPPORTED_LOCALES']:
        return locale
    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Index"""
    return render_template(
        '4-index.html',
        locale=get_locale()
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
