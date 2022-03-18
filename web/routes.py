from flask import Blueprint, render_template, redirect, url_for
from extensions import *

web = Blueprint("web", __name__, template_folder=web)

@web.route('/')
def index_add_event():
    # Creating meeting page
    return render_template('add_events.html')

