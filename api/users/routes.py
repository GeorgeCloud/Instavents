from flask import Blueprint, request, jsonify
from api.extensions import *

user = Blueprint("user", __name__)

@user.route('/', methods=['GET'])
def index():
    all_users = []
    for user in users.find():
        all_users.append({'_id': user['_id'], 'name' : user['name'], 'phone_number': user['phone_number']})
    return jsonify({'result' : all_users})

@user.route('/<user_id>', methods=['GET'])
def get_one_user(user_id):
    user = users.find_one({'_id': user_id})
    if user:
        del user['password']
        return jsonify({'result': user}), 200

    return jsonify({'result' : 'User is not found'}), 404

#What if user signin => signin route
#What if user signin => signup route
