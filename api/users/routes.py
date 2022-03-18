from flask import Blueprint, request, jsonify
from extensions import *

user = Blueprint("user", __name__)

@user.route('/', methods=['GET'])
def index():
    all_users = users.find({})
    return render_template('users.html', users=all_users)

# If signed in
@user.route('/<user_id>', methods=['GET'])
def show_user(user_id):
    user = users.find_one({'_id': user_id})

    if user:
        user_events = [e for e in events.find({'owner_id': user_id})]
        return render_template('show_user.html', user=user, events=user_events)

    return 'user does not exist'
