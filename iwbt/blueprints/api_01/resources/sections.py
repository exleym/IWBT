"""
    API Routes for <Section> Resource
    ===================================================================
    These routes serve as endpoints for performing CRUD operations on
    the <Section> resources. Sections are stretches of `rivers` that
    are individually demarcated, and generally run as a single chunk.

    Section names need not be unique, but should be unique to a river.
    i.e. there shouldn't be two instances representing Section IV of
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

from iwbt.blueprints.api_01 import api_01, error_out, verify_required_fields


@api_01.route('/section', methods=['POST'])
def create_section():
    """ POST to /api/section will create a new Section object in the database
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['name', 'river_id']

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(request.json, expected_fields):
        return error_out(PostValidationError())
    name = request.json['name']
    river_id = request.json['river_id']
    session = get_session(current_app)
    section = Section(**request.json)
    session.add(section)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    section = session.query(Section).filter(Section.name == name) \
                                    .filter(River.id == river_id).first()
    return jsonify(section.shallow_json), 200


@api_01.route('/sections/', methods=['GET'])
def read_sections():
    """ GET /api/sections returns shallow json of Sections
    """
    session = get_session(current_app)
    sections = session.query(Section).all()
    return jsonify([section.shallow_json for section in sections]), 200