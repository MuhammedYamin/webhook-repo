from flask_pymongo import PyMongo

mongo = PyMongo()

def init_extensions(app):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/webhookdb"
    mongo.init_app(app)
