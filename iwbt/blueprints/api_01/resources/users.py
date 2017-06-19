from flask import current_app, jsonify, request
from flask_login import current_user
from iwbt import get_db, get_session
from iwbt.models.social import (PaddleLogEntry,
                                User,
                                Trip,
                                associate_user_favorites)
from iwbt.models.rivers import River, Section
from iwbt.util.api_errors import (DatabaseIntegrityError,
                                  MissingResourceError,
                                  MissingJSONError,
                                  PostValidationError)

from iwbt.blueprints.api_01 import api_01, error_out, verify_required_fields

# Social Functionality via API
# The social aspect of this application is centered on the concept of the Trip
# and PaddleLogEntry. User objects and Trip objects are the vectors through
# which we can retrieve Logs. JSON properties for both User and Trip will
# contain a 'logs' field which is an array of serialized log objects.
# Logs can also be retrieved directly by their id value or indirectly by the
# get_user_logs_by_id() route ('/user/<int:user_id>/logs') and
# get_user_logs_by_alias() route ('/user/<string:alias>/logs')
@api_01.route('/log/<int:entry_id>', methods=['GET'])
def get_log_by_id(entry_id):
    session = get_session(current_app)
    log = session.query(PaddleLogEntry) \
                 .filter(PaddleLogEntry.id == entry_id).first()
    return jsonify(log.json)


@api_01.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    session = get_session(current_app)
    user = session.query(User).filter(User.id == user_id).first()
    return jsonify(user.json)


@api_01.route('/user/<string:alias>', methods=['GET'])
def get_user_by_alias(alias):
    session = get_session(current_app)
    user = session.query(User).filter(User.alias == alias).first()
    return jsonify(user.json)


@api_01.route('/user/<int:user_id>/logs', methods=['GET'])
def get_user_logs_by_id(user_id):
    session = get_session(current_app)
    user = session.query(User).filter(User.id == user_id).first()
    return jsonify(user.json)


@api_01.route('/user/<string:alias>/logs', methods=['GET'])
def get_user_logs_by_alias(alias):
    session = get_session(current_app)
    user = session.query(User).filter(User.alias == alias).first()
    return jsonify(user.json)


@api_01.route('/log/create', methods=['POST'])
def add_log_entry():
    if not request.json:
        return error_out(MissingJSONError())
    session = get_session(current_app)
    user_alias = request.json['user_alias'] or None
    if user_alias:
        user = session.query(User).filter(User.alias == request.json['user_alias']).one()
    else:
        user = current_user
    trip = session.query(Trip).filter(Trip.id == request.json['trip_id']).one()
    river = session.query(River).filter(River.id == request.json['river_id']).one()
    section = session.query(Section).filter(Section.id == request.json['section_id']).one()
    entry = PaddleLogEntry(user_id=user.id,
                           trip_id=trip.id,
                           river_id=river.id,
                           section_id=section.id,
                           public=True)
    session.add(entry)
    session.commit()
    return jsonify(200)


@api_01.route('/user/<int:user_id>/favorite/<river_id>', methods=['POST'])
def add_favorite_river(user_id, river_id):
    insert = associate_user_favorites.insert().values(
        user_id=user_id,
        river_id=river_id
    )
    con = get_db(current_app)
    con.execute(insert)
    return jsonify(200)