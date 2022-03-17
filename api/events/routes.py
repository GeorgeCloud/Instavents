from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from api.extensions import *
import uuid

event = Blueprint("event", __name__)

@event.route('/', methods=['GET'])
def index():
    output = [event for event in events.find()]

    return jsonify({'meetings result' : output}), 200

@event.route('/create', methods=['POST'])
def create_event():
    owner_id = request.json['owner_id'] or None
    owner_name = request.json['name']
    event_name = request.json['event_name']
    recipients = request.json['recipients']
    date = request.json['date']
    time = request.json['time']
    contacts = {}

    for name, phone_number in recipients.items():
        if validate_number(phone_number):
            contacts[name] = phone_number

    event_id = events.insert_one({'_id': uuid.uuid4().hex, 'owner_id': owner_id, 'name': owner_name, 'event_name': event_name, 'date': date, 'recipients': contacts, 'time': time}).inserted_id
    new_event = events.find_one({'_id' : event_id})
    return jsonify(new_event), 200

#If signed in
@event.route('/user/<user_id>', methods=['GET'])
def get_events_by_user(user_id):
    output = [e for e in events.find({'owner_id': user_id})]
    if output:
        return jsonify({'events result' : output}), 200

    return jsonify({'events result' : 'not found'}), 404

@event.route('/<event_id>', methods=['GET'])
def show_event(event_id):
    event = events.find_one({'_id': event_id})
    if event:
        return jsonify({'event result' : event}), 200

    return jsonify({'event result' : 'not found'}), 404

