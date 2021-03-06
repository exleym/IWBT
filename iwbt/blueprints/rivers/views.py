from flask import Blueprint, current_app, render_template, redirect, request, url_for, flash

from flask_login import login_user, logout_user, login_required, current_user

from iwbt import get_session
from iwbt.models.rivers import *

rivers = Blueprint('rivers', __name__, url_prefix='river')


@rivers.route('/list')
def river_list():
    session = get_session(current_app)
    rivers = session.query(River).all()
    return render_template('rivers/river_list.html', rivers=rivers)


@rivers.route('/<int:river_id>')
def river_page(river_id):
    session = get_session(current_app)
    river = session.query(River).filter(River.id == river_id).first()
    return render_template('rivers/river_main.html', river=river)


@rivers.route('/favorites')
@login_required
def favorites():
    session = get_session(current_app)
    return render_template('rivers/river_list.html', rivers=current_user.favorite_rivers)