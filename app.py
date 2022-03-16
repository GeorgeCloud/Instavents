from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

from api.auth.routes import auth
from api.main.routes import main
from api.events.routes import event

app = Flask(__name__)
app.secret_key = 'georgeandahyeon777'

app.register_blueprint(main, url_prefix="/users")
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(event, url_prefix="/events")

 
if __name__ == '__main__':
    app.run(debug=True)
