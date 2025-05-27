import os
from flask import Flask
from trade_backend.middleware.response_middleware import response_middleware
from trade_backend.futures.routes import futures_bp


def register_blueprint(app):
    app.register_blueprint(
        futures_bp,
        url_prefix="/api/futures",
    )
    return app


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.after_request(response_middleware)
    register_blueprint(app)
    return app
