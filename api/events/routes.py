from flask import Blueprint
from api.extensions import *

events = Blueprint("events", __name__)

@events.route('/', methods=['GET'])
def index():
    return 'All events'

