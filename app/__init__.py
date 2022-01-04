import os

from flask import Flask, redirect, url_for, g
from . import db, auth, calendar


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        debug=True,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(calendar.bp)

    @app.errorhandler(404)
    def page_not_found(e):
        if g.user:
            return redirect(url_for("calendar.redirect_day_view"))
        else:
            return redirect(url_for("auth.login"))

    return app


# set FLASK_APP=app
# set FLASK_ENV=development
# flask run


#http://127.0.0.1:5000/auth/register


# Zorran
# Valopant