import os

from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', #TODO: Change me
        DEBUG = True,
        SQLALCHEMY_DATABASE_URI='sqlite:///astrarium.db',
        SQLALCHEMY_TRACK_MODIFICATIONS = False
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

    from apps.database import db
    db.init_app(app)
    
    # import apps.forms
    # app.register_blueprint(forms.bp)

    CORS(app)
    
    return app
