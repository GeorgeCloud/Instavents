from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from bson.objectid import ObjectId
from api.twilio_api import create_rsvp
from extensions import *
import uuid

event = Blueprint("event", __name__)

@event.route('/', methods=['GET'])
def index():
    output = [event for event in events.find()]
    return output

@event.route('/new')
def new_event():
    return render_template('events_new.html')

# http://127.0.0.1:5000/events/rsvp/e4a77b17191842fea244d1c484b936b2
@event.route('/rsvp/<rsvp_id>', methods=['GET', 'POST'])
def event_response(rsvp_id):
    rsvp = rsvps.find_one({'_id': rsvp_id})

    if not rsvp:
        flash('Invitation is expired or invalid')
        return redirect(url_for('auth.signin'))

    event = events.find_one({'_id': rsvp['event_id']})

    if request.method == 'GET':
        return render_template('events_respond.html', event=event)

    response = True if request.form.get('response') == 'true' else False

    rsvps.update_one({'_id': rsvp_id}, {'$set':{'status': response}})

    return 'Thank you for your response! You may close this page'

@event.route('/create', methods=['POST'])
def create_event():
    owner_id          = session['current_user']['_id'] if 'current_user' in session else None
    owner_name        = request.form['owner_name']
    event_name        = request.form['event_name']
    phone_number      = request.form['phone_number']
    date              = request.form['date']
    time              = request.form['time']
    recipient_name1   = request.form.get('recipient_name1')
    recipient_number1 = request.form.get('recipient_number1')
    recipient_name2   = request.form.get('recipient_name2')
    recipient_number2 = request.form.get('recipient_number2')
    recipients        = []

    if recipient_name1 and recipient_number1:
        recipients.append({'name': recipient_name1, 'number': recipient_number1})

    new_event = {
        '_id':         uuid.uuid4().hex,
        'owner_id':    owner_id,
        'owner_name':  owner_name,
        'owner_number': phone_number,
        'name':        event_name,
        'rsvps':       [],
        'date':        date,
        'time':        time
    }

    event_id  = events.insert_one(new_event).inserted_id
    # event     = events.find_one({'_id' : event_id})

    for recipient in recipients:
        create_rsvp(recipient, event_id)

    return redirect(url_for('event.show_event', event_id=event_id))

@event.route('/<event_id>', methods=['GET'])
def show_event(event_id):
    event = events.find_one({'_id': event_id})
    event_rsvps = rsvps.find({'event_id': event_id})

    return render_template('events_show.html', event=event, rsvps=event_rsvps)
