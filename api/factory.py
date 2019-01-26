import os

from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')


def create_app(app_name):
    app = Flask(app_name)
    configure_mongo(app)
    configure_blueprints(app)
    return app


def configure_blueprints(application):
    from api.app.api import api_bp
    application.register_blueprint(api_bp)


def configure_mongo(app):
    app.config["MONGO_URI"] = "mongodb://root:example@{}:27017/gamelog?authSource=admin".format(DATABASE_HOST)
    mongo.init_app(app)
