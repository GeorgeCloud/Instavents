from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from api.extensions import *
import uuid

event = Blueprint("event", __name__)

@event.route('/', methods=['GET'])
def get_events():
    event_result = []
    for event in events.find():
        event_result.append({'name' : event['name'], 'meeting_name': event['meeting_name'], 'date': event['date'], 'time': event['time']})

    return jsonify({'meetings result' : event_result})

@event.route('/<meeting_id>', methods=['GET'])
def get_one_event(meeting_id):
    event = events.find_one({'_id': meeting_id})

    if event:
        output = event
    else:
        output = 'event is not found'
    
    return jsonify({'event result' : output})

@event.route('/', methods=['POST'])
def add_one_event():
    name = request.json['name']
    meeting_name = request.json['meeting_name']
    date = request.json['date']
    time = request.json['time']

    event_id = events.insert_one({'_id': uuid.uuid4().hex, 'name': name, 'meeting_name': meeting_name, 'date': date, 'time': time }).inserted_id
    find_event = events.find_one({'_id' : event_id})
    return jsonify(find_event)

    # contact_id
