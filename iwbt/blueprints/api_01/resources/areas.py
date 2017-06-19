from flask import current_app, jsonify, request
from iwbt import get_session
from iwbt.models.rivers import *
from iwbt.util.api_errors import (DatabaseIntegrityError,
                                  MissingResourceError,
                                  MissingJSONError,
                                  PostValidationError)

from iwbt.blueprints.api_01 import api_01, error_out, verify_required_fields


# API Routes for accessing and managing area information
# With these API endpoints, users can retrieve area information by id,
# retrieve a list of areas, add new areas, update existing areas.
@api_01.route('/area', methods=['POST'])
def create_area():
    """ POST to /api/v1.0/areas will create a new Area object in the database
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['name']

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(request.json, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    area = Area(name=request.json['name'])
    session.add(area)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    name = request.json['name']
    area = session.query(Area).filter(Area.name == name).first()
    return jsonify(area.shallow_json)


@api_01.route('/area/<int:area_id>', methods=['GET'])
def read_area_by_id(area_id):
    session = get_session(current_app)
    area = session.query(Area).filter(Area.id == area_id).first()
    if not area:
        return error_out(MissingResourceError('Area'))
    return jsonify(area.shallow_json)


@api_01.route('/areas/', methods=['GET'])
def read_areas():
    session = get_session(current_app)
    areas = session.query(Area).all()
    if not areas:
        return error_out(MissingResourceError('Area'))
    return jsonify([area.shallow_json for area in areas])


@api_01.route('/area/<int:area_id>', methods=['PUT'])
def update_area(area_id):
    """ PUT request to /api/area/<area_id> will update Area object <id> with
        fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    area = session.query(Area).filter(Area.id == area_id).first()
    if not area:
        return error_out(MissingResourceError('Area'))
    for k, v in put_data.iteritems():
        setattr(area, k, v)
    session.add(area)
    session.commit()
    return jsonify(area.shallow_json)


@api_01.route('/area/<int:area_id>', methods=['DELETE'])
def delete_area(area_id):
    """ DELETE request to /api/v1.0/area/<area_id> will delete the target Area
        object from the database
    """
    session = get_session(current_app)
    area = session.query(Area).filter(Area.id == area_id).first()
    if not area:
        return error_out(MissingResourceError('Area'))
    session.delete(area)
    session.commit()
    return jsonify(200)