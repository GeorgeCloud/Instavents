from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash, session
from bson.objectid import ObjectId
from extensions import *
import uuid
import bcrypt
from utils import validate_number

auth = Blueprint("auth", __name__)

@auth.route('/', methods=['GET'])
def index():
    return redirect(url_for('event.new_event'))

@auth.route('/dashboard', methods=['GET'])
def dashboard():
    if 'current_user' in session:
        user = users.find_one({'phone_number': session['current_user']['phone_number']})
        user_events = [e for e in events.find({'owner_id': user['_id']})]

        return render_template('dashboard.html', events=user_events)

    return redirect(url_for('auth.signin'))

@auth.route('/signup', methods=['GET', 'POST']) # Sign up Page
def signup():
    if 'current_user' in session: return redirect(url_for('auth.dashboard'))
    if request.method == 'GET': return render_template('signup.html')

    name = request.form['name']
    phone_number = request.form['phone_number']
    password = request.form['password']

    if users.find_one({'phone_number': phone_number}):
        flash('The phone number already exists')
        return redirect(request.referrer)

    if validate_number(phone_number): # +1 123-456-7890
        if len(password) <= 8:
            flash('Password needs to be minimum 8 characters')
            return redirect(request.referrer)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_id = users.insert_one({
            '_id': uuid.uuid4().hex,
            'name': name,
            'phone_number': phone_number,
            'password': hashed_password
        }).inserted_id

        flash('Account was successfully created')
        return redirect(url_for('auth.signin'))
    else:
        flash('Invalid Phone Number')
        return redirect(request.referrer)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'current_user' in session: return redirect(url_for('auth.dashboard'))
    if request.method == 'GET': return render_template('signin.html')

    phone_number = request.form['phone_number']
    user = users.find_one({'phone_number' : phone_number})
    if user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), user['password']) == user['password']:
            del user['password']
            session['current_user'] = user
            flash('Signed In')
            return redirect(url_for('auth.dashboard'))

    flash('Invalid email/password combination')
    return redirect(request.referrer)

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'current_user' in session:
        session.pop('current_user', None)
    return redirect(url_for('auth.signin'))
