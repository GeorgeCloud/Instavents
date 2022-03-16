from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from api.extensions import *
import uuid

event = Blueprint("event", __name__)

@event.route('/', methods=['GET'])
def index():
    output = [event for event in events.find()]

    return jsonify({'meetings result' : output}), 200

@event.route('/user/<user_id>', methods=['GET'])
def get_events_by_user(user_id):
    output = [e for e in events.find({'owner_id': user_id})]
    if output:
        return jsonify({'meetings result' : output}), 200

    return jsonify({'event result' : 'not found'}), 404

@event.route('/<event_id>', methods=['GET'])
def show_event(event_id):
    event = events.find_one({'_id': event_id})
    if event:
        return jsonify({'event result' : event}), 200

    return jsonify({'event result' : 'not found'}), 404

@event.route('/new', methods=['POST'])
def new_event():
    owner_id = request.json['owner_id'] or None
    name = request.json['name']
    event_name = request.json['event_name']
    recipients = request.json['recipients']
    date = request.json['date']
    time = request.json['time']

    event_id = events.insert_one({'_id': uuid.uuid4().hex, owner_id: None, 'name': name, 'event_name': event_name, 'date': date, 'recipients': recipients, 'time': time}).inserted_id

    new_event = events.find_one({'_id' : event_id})
    return jsonify(new_event), 200
