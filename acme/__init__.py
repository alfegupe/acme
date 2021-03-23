from config import Config
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False, template_folder='../templates')
    app.config.from_object(config_class)
    mongo.init_app(app)

    return app
