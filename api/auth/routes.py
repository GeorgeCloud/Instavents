from flask import Blueprint, redirect, url_for
from api.extensions import *

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET']) # Sign up Page
def signup(): 
    return 'Signup Page'

@auth.route('/login', methods=['GET'])
def login():
    return 'Login Page'

@auth.route('/logout', methods=['GET'])  # Change to post after 
def logout():
    return redirect(url_for('auth.login'))

