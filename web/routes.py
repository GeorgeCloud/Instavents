from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session
from bson.objectid import ObjectId
from extensions import *
import uuid
import bcrypt

main = Blueprint("main", __name__)

@main.route('/')
def index_add_event():
    # Creating meeting page
    return render_template('add_events.html')
