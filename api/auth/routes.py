from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from bson.objectid import ObjectId
from extensions import *
import uuid
import bcrypt
from utils import validate_number

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST']) # Sign up Page
def signup():
    if 'current_user' in session:
        return render_template('dashboard.html')

    if request.method == 'GET':
        return render_template('signup.html')

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
    if 'current_user' in session:
        flash('You are already signed in')
        return render_template('dashboard.html')

    if request.method == 'GET':
        return render_template('signin.html')

    phone_number = request.form['phone_number']
    user = users.find_one({'phone_number' : phone_number})
    if user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), user['password']) == user['password']:
            session['current_user'] = user
            flash('Signed In')
            return render_template('dashboard.html')

    flash('Invalid email/password combination')
    return redirect(request.referrer)

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'current_user' in session:
        session.pop('current_user', None)
    return redirect(url_for('auth.signin'))
