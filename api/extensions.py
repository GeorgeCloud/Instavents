from pymongo import MongoClient
import os
import re

uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/instavents')
client = MongoClient(uri)
db = client.InstaVents

users = db.users
users.create_index("phone_number", unique=True)
events = db.events

def validate_number(number):
    if re.search(r'^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', number):
        return True
    else:
        return False
    