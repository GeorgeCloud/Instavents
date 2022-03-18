from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from api.twilio_api import create_rsvp
from extensions import *
import uuid

event = Blueprint("event", __name__)

@event.route('/', methods=['GET'])
def index():
    output = [event for event in events.find()]
    return jsonify({'meetings result' : output}), 200

@event.route('/create', methods=['POST'])
def create_event():
    owner_id   = request.json.get('owner_id') or None
    owner_name = request.json['name']
    event_name = request.json['event_name']
    recipients = request.json.get('recipients') or []
    date       = request.json['date']
    time       = request.json['time']

    new_event = {
        '_id':        uuid.uuid4().hex,
        'owner_id':   owner_id,
        'name':       owner_name,
        'event_name': event_name,
        'rsvps':      [],
        'date':       date,
        'time':       time
    }

    event_id  = events.insert_one(new_event).inserted_id
    event     = events.find_one({'_id' : event_id})

    for recipient in recipients:
        create_rsvp(recipient, event_id)

    return jsonify(event), 200

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
    return render_template('events_show')
