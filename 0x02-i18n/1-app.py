#!/usr/bin/env python3
""" Basic Babel setup"""

from flask import Flask, render_template
from flask_babel import Babel, _


app = Flask(__name__)


class Config:
    """Config class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)

babel = Babel(app)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Index"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
