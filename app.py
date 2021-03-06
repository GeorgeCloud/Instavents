from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

from api.auth.routes import auth
from api.users.routes import user
from api.events.routes import event
from web.routes import main
import os

app = Flask(__name__, template_folder="web/templates")
app.secret_key = os.getenv('SECRET_KEY')

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(user, url_prefix='/users')
app.register_blueprint(event, url_prefix='/events')

if __name__ == '__main__':
    app.run(debug=True)
