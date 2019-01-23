from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app(app_name):
    app = Flask(app_name)
    configure_mongo(app)
    configure_blueprints(app)
    return app


def configure_blueprints(app):
    from api.app.api import api_bp
    app.register_blueprint(api_bp)


def configure_mongo(app):
    app.config["MONGO_URI"] = "mongodb://root:example@localhost:27017/gamelog?authSource=admin"
    mongo.init_app(app)
