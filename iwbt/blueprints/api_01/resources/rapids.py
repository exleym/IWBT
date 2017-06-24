"""
    API Routes for <Rapid> Resource
    ===================================================================
    These routes serve as endpoints for performing CRUD operations on
    the <Rapid> resources. Rapids are currently the smallest piece of
    the systems we are modeling and are generally a single nonstop
    piece of whitewater.

    Rapid names need not be unique, but should be unique to a river.
    i.e. there shouldn't be two instances representing Bull Sluice on
    the Chattooga river. To this effect, the API endpoints that create
    new sections must check that the specific resource does not already
    exist, and if it does, should return a preemptive
    DatabaseIntegrityError.
"""
from flask import current_app, jsonify, request
from iwbt import get_session
from iwbt.models.rivers import *
from iwbt.util.api_errors import (DatabaseIntegrityError,
                                  MissingResourceError,
                                  MissingJSONError,
                                  PostValidationError)

from iwbt.blueprints.api_01 import api_01, error_out, verify


@api_01.route('/rapid', methods=['POST'])
def create_rapid():
    """ POST to /api/section will create a new Section object in the database
    """
    if not request.json:
        return error_out(MissingJSONError())
    required_fields = ['name', 'river_id', 'section_id']
    allowed_fields = ['rating']

    # Ensure that required fields have been included in JSON data
    if not verify(request.json, required_fields, allowed_fields):
        return error_out(PostValidationError())
    name = request.json['name']
    river_id = request.json['river_id']
    session = get_session(current_app)
    rapid = Rapid(**request.json)
    session.add(rapid)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    rapid = session.query(Rapid).filter(Rapid.name == name) \
                                .filter(River.id == river_id).first()
    return jsonify(rapid.shallow_json), 200