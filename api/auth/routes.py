from flask import Blueprint, redirect, url_for, request, jsonify, session
from api.extensions import *
from bson.objectid import ObjectId
import uuid
import bcrypt

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['POST']) # Sign up Page
def signup():
    name = request.json['name']
    phone_number = request.json['phone_number']
    password = request.json['password']

    if users.find_one({'phone_number': phone_number}):
        return jsonify({'Error' : 'The phone number already exists!'})

    if len(password) < 8:
        return jsonify({'Error' : 'Password needs to be minimum 8 characters'})

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if len(phone_number) == 12: # +1 123-456-7890
        user_id = users.insert_one({
            '_id': uuid.uuid4().hex,
            'name': name,
            'phone_number': phone_number,
            'password': hashed_password
        }).inserted_id

        new_user = users.find_one({'_id': user_id})
        session['current_user'] = new_user
        return jsonify([{'name' : new_user['name'], 'phone_number': new_user['phone_number']}])
    else:
        return jsonify({'Error' : 'Type the correct number'})

@auth.route('/signin', methods=['POST'])
def signin():
    phone_number = request.json['phone_number']
    user = users.find_one({'phone_number' : phone_number})
    if user:
        if bcrypt.hashpw(request.json['password'].encode('utf-8'), user['password']) == user['password']:
            session['current_user'] = user
            return jsonify([{'name' : user['name'], 'phone_number': user['phone_number']}])

    return jsonify({'message' : 'Invalid email/password combination'})

@auth.route('/logout', methods=['POST'])
def logout():
    if 'current_user' in session:
        session.pop('current_user', None)
    return jsonify({'message' : 'You successfully logged out'})
