from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user
from iwbt import get_session
from iwbt.models.rivers import *
from iwbt.models.social import *

api_01 = Blueprint('api_01', __name__, url_prefix='api')


# API Routes for accessing river information
# With these API endpoints, users can retrieve river information by id or name
# as well as get all rivers, get their favorite rivers, get another user's favorite
# rivers, and add a new river to the database.
# TODO: test the add river feature with PostMan
# TODO: install the requests python library
@api_01.route('/river/<int:river_id>', methods=['GET'])
def get_river_by_id(river_id):
    session = get_session(current_app)
    river = session.query(River).filter(River.id == river_id).first()
    print river.json
    return jsonify(river.json)


@api_01.route('/river/<string:river_name>', methods=['GET'])
def get_river_by_name(river_name):
    session = get_session(current_app)
    river = session.query(River).filter(River.name == river_name).first()
    return jsonify(river.json)


@api_01.route('/rivers/', methods=['GET'])
def get_rivers():
    session = get_session(current_app)
    rivers = session.query(River).all()
    return jsonify([river.json for river in rivers])


@api_01.route('/river/create', methods=['POST'])
def add_river():
    if not request.json:
        return jsonify({'ErrorCode': 500, 'ErrorMessage': 'You must post JSON to create a new River'})
    session = get_session(current_app)
    river = River(**request.json)
    session.add(river)
    session.commit()
    return jsonify(200)


# Perhipheral river functionality
# River-related queries that are not pulling the actual river objects
@api_01.route('/river/<int:river_id>/flow', methods=['GET'])
def check_flow_by_river_id(river_id):
    session = get_session(current_app)
    river = session.query(River).filter(River.id == river_id).first()
    return jsonify(river.current_flow)



# Social Functionality via API
# The social aspect of this application is centered on the concept of the Trip and PaddleLogEntry
# User objects and Trip objects are the vectors through which we can retrieve Logs
# json properties for both User and Trip will contain a 'logs' field which is an array of serialized
# log objects. Logs can also be retrieved directly by their id value or indirectly by the get_user_logs_by_id()
# route ('/user/<int:user_id>/logs') and get_user_logs_by_alias() route ('/user/<string:alias>/logs')
@api_01.route('/log/<int:entry_id>')
def get_log_by_id(entry_id):
    session = get_session(current_app)
    log = session.query(PaddleLogEntry).filter(PaddleLogEntry.id == entry_id).first()
    return jsonify(log.json)


@api_01.route('/user/<int:user_id>')
def get_user_by_id(user_id):
    session = get_session(current_app)
    user = session.query(User).filter(User.id == user_id).first()
    return jsonify(user.json)


@api_01.route('/user/<string:alias>')
def get_user_by_alias(alias):
    session = get_session(current_app)
    user = session.query(User).filter(User.alias == alias).first()
    return jsonify(user.json)


@api_01.route('/user/<int:user_id>/logs')
def get_user_logs_by_id(user_id):
    session = get_session(current_app)
    user = session.query(User).filter(User.id == user_id).first()
    return jsonify(user.json)


@api_01.route('/user/<string:alias>/logs')
def get_user_logs_by_alias(alias):
    session = get_session(current_app)
    user = session.query(User).filter(User.alias == alias).first()
    return jsonify(user.json)


@api_01.route('/log/create', methods=['POST'])
def add_log_entry():
    if not request.json:
        return jsonify({'ErrorCode': 500, 'ErrorMessage': 'You must post JSON to create a new River'})
    session = get_session(current_app)
    user_alias = request.json['user_alias'] or None
    if user_alias:
        user = session.query(User).filter(User.alias == request.json['user_alias']).one()
    else:
        user = current_user
    trip = session.query(Trip).filter(Trip.id == request.json['trip_id']).one()
    river = session.query(River).filter(River.id == request.json['river_id']).one()
    section = session.query(Section).filter(Section.id == request.json['section_id']).one()
    entry = PaddleLogEntry(user_id=user.id, trip_id=trip.id, river_id=river.id, section_id=section.id, public=True)
    session.add(entry)
    session.commit()
    return jsonify(200)