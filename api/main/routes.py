from flask import Blueprint, request
from api.extensions import *

main = Blueprint("main", __name__) 

@main.route('/', methods=['GET'])
def index():
    all_users = []
    for user in users.find():
        all_users.append({'name' : user['name'], 'phone_number': user['phone_number'], 'password': user['password']})
    return jsonify({'result' : all_users})

@main.route('/<phone_number>', methods=['GET'])
def get_one_user(name):
    find_user = users.find_one({'name': name})

    if find_user:
        output = {'name' : find_user['name'], 'phone_number': find_user['phone_number'], 'password': find_user['password']}
    else:
        output = 'User is not found'
    
    return jsonify({'result' : output})
