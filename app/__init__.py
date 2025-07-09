from flask import Flask
from flask_pymongo import PyMongo
from app.extensions import mongo, init_extensions


def create_app(template_folder=None):
    app = Flask(__name__, template_folder=template_folder)

    init_extensions(app) 

    from app.webhook.routes import webhook
    app.register_blueprint(webhook)

    return app
