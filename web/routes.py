from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session
from bson.objectid import ObjectId
from extensions import *
import uuid
import bcrypt
import requests

main = Blueprint("main", __name__)

api_url = 'http://localhost:5000/api'

@main.route('/')
def index():
    return redirect(url_for('main.new_event'))

@main.route('/new-event', methods=['GET', 'POST'])
def new_event():
    # Creating meeting page
    if request.method == 'GET':
        return render_template('dashboard.html')

    # Post to api/events/create | event.create_event
    res = requests.post(f'{api_url}/events/create', json=request.form.to_dict(flat=False))
    return redirect(url_for('main.create_rsvp'))

@main.route('/add-user', methods=['GET', 'POST'])
def create_rsvp():
    # Creating meeting page
    if request.method == 'GET':
        return render_template('contact_lists.html')

    # Post to api/events/create | event.create_event
    json_data = request.form.to_dict(flat=False)
    json_data['recipient_name']
    res = requests.post(f'{api_url}/events/create', json=json_data)
    return render_template('contact_lists.html')
