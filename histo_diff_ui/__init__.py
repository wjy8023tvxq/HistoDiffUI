import os

from flask import Flask
from flask_pymongo import PyMongo


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Config MongoDB URI
    app.config["MONGO_URI"] = "mongodb://wjy8023tvxq:vhWpnyIXZounFSUZ@localhost:27017/"

    # Initialize PyMongo
    mongo = PyMongo(app)

    app.config.from_mapping(SECRET_KEY='dev')

    # register app blueprints
    from views import main_routes
    app.register_blueprint(main_routes)

    return app
