from pymongo import MongoClient
import os

uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/instavents')
client = MongoClient(uri)
db = client.InstaVents

users = db.users
users.create_index("phone_number", unique=True)
events = db.events
rsvps = db.rsvps
