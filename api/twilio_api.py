from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
from utils import validate_number
from extensions import *
import uuid
import os

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(account_sid, auth_token)

def create_rsvp(recipients, event_id):
    # TODO: Validate unqiue entry: phone_number & event_id
    for recipient, phone_number in recipients.items():
        if validate_number(phone_number):
            new_rsvp = {
                '_id': uuid.uuid4().hex,
                'event_id': event_id,
                'recipient_name': recipient,
                'recipient_phone_number': phone_number,
                'status': None,
                'created_on': datetime.now()
            }

            rsvp_id = rsvps.insert_one(new_rsvp).inserted_id
            events.update_one(
               { '_id': event_id },
               { '$addToSet': { 'rsvps': rsvp_id } }
            )

            client.messages.create(
                to=f'{phone_number}',
                from_=f'{twilio_phone_number}',
                body=f'https://instavents.herokuapp.com/rsvp/{rsvp_id}'
            )
