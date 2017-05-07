from flask import Blueprint, current_app, render_template, redirect, request, url_for, flash

from flask_login import login_user, logout_user, login_required, current_user

from iwbt import get_session
from iwbt.models.rivers import *

rivers = Blueprint('rivers', __name__, url_prefix='river')


@rivers.route('/<name>')
def user_page(name):
    session = get_session(current_app)
    river = session.query(River).filter(River.name == name).first()
    print river
    return render_template('rivers/river_main.html', river=river)