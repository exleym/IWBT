from flask import current_app, jsonify, request
from iwbt import get_session
from iwbt.models.rivers import *
from iwbt.util.api_errors import (DatabaseIntegrityError,
                                  MissingResourceError,
                                  MissingJSONError,
                                  PostValidationError)

from iwbt.blueprints.api_01 import api_01, error_out, verify_required_fields


# API Routes for accessing and managing river information
# With these API endpoints, users can retrieve river information by id or name,
# retrieve a list of rivers, add new rivers, update existing rivers.
@api_01.route('/river', methods=['POST'])
def create_river():
    """ POST to /api/rivers will create a new River object in the database
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['name', 'area_id']

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(request.json, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    river = River(**request.json)
    session.add(river)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    name = request.json['name']
    river = session.query(River).filter(River.name == name).first()
    response = jsonify()
    response.data = jsonify(river.json)
    response.headers['Access-Control-Allow-Origin'] = request.headers['Access-Control-Allow-Origin']
    return jsonify(river.json)


@api_01.route('/river/<int:river_id>', methods=['GET'])
def read_river_by_id(river_id):
    session = get_session(current_app)
    river = session.query(River).filter(River.id == river_id).first()
    if not river:
        return error_out(MissingResourceError('River'))
    return jsonify(river.json)


@api_01.route('/river/<string:river_name>', methods=['GET'])
def read_river_by_name(river_name):
    session = get_session(current_app)
    river = session.query(River).filter(River.name == river_name).first()
    if not river:
        return error_out(MissingResourceError('River'))
    return jsonify(river.json)


@api_01.route('/rivers/', methods=['GET'])
def read_rivers():
    session = get_session(current_app)
    rivers = session.query(River).all()
    if not rivers:
        return error_out(MissingResourceError('River'))
    return jsonify([river.json for river in rivers])


@api_01.route('/river/<int:river_id>', methods=['PUT'])
def update_river(river_id):
    """ PUT request to /api/river/<river_id> will update River object <id>
        with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    river = session.query(River).filter(River.id == river_id).first()
    if not river:
        return error_out(MissingResourceError('River'))
    for k, v in put_data.iteritems():
        setattr(river, k, v)
    session.add(river)
    session.commit()
    return jsonify(river.shallow_json)


@api_01.route('/river/<int:river_id>', methods=['DELETE'])
def delete_river(river_id):
    session = get_session(current_app)
    river = session.query(River).filter(River.id == river_id).first()
    if not river:
        return error_out(MissingResourceError('River'))
    session.delete(river)
    session.commit()
    return jsonify(200)
