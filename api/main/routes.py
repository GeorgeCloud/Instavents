from flask import Blueprint, request
from api.extensions import *

main = Blueprint("main", __name__) 

@main.route('/', methods=['GET'])
def index():
    return 'All users'
