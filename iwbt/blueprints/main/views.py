from flask import Blueprint, current_app, render_template, redirect, request, url_for, flash

from flask_login import login_user, logout_user, login_required, current_user

from iwbt import get_session
from iwbt.models.rivers import *

main = Blueprint('main', __name__, url_prefix='')


@main.route('/')
def index():
    session = get_session(current_app)
    return render_template('index.html')
