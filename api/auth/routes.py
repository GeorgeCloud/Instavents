from flask import Blueprint, redirect, url_for, request, jsonify
from api.extensions import *
from bson.objectid import ObjectId
import uuid
import bcrypt

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['POST']) # Sign up Page
def signup():
    name = request.json['name']
    phone_number = request.json['phone_number']
    user_exists = users.find_one({'phone_number': phone_number})

    if user_exists:
        return({'Error' : 'The phone number already exists!'})

    password = request.json['password']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if len(phone_number) == 12: # +1 123-456-7890
        user_id = users.insert_one({
            '_id': uuid.uuid4().hex, 'name': name, 'phone_number': phone_number,
            'password': hashed_password }
        ).inserted_id

        new_user = users.find_one({'_id': user_id})
        return jsonify([{'name' : new_user['name'], 'phone_number': new_user['phone_number']}])
    else:
        return({'Error' : 'Type the correct number'})

@auth.route('/login', methods=['GET'])
def login():
    return 'Login Page'

@auth.route('/logout', methods=['GET'])  # Change to post after
def logout():
    return redirect(url_for('auth.login'))

@auth.route('/', methods=['GET'])
def get_users():
    output = []
    for user in users.find():
        output.append({'name' : user['name'], 'phone_number': user['phone_number'], 'password': user['password']})
    return jsonify({'result' : output})
