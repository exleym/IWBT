from flask import current_app, jsonify, request
from iwbt import get_session
from iwbt.models.rivers import *
from iwbt.util.api_errors import (DatabaseIntegrityError,
                                  MissingResourceError,
                                  MissingJSONError,
                                  PostValidationError)

from iwbt.blueprints.api_01 import api_01, error_out, verify_required_fields


# API Routes for accessing and managing gauge information
# With these API endpoints, users can retrieve gauge information by id,
# retrieve a list of gauges, add new gauges, update existing gauges.
@api_01.route('/gauge', methods=['POST'])
def create_gauge():
    """ POSTing to /api/gauges will create a new Gauge object in the database
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['usgs_id', 'name', 'river_id']
    if not verify_required_fields(request.json, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    gauge = Gauge(**request.json)
    session.add(gauge)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    name = request.json['name']
    gauge = session.query(Gauge).filter(Gauge.name == name).first()
    return jsonify(gauge.shallow_json)


@api_01.route('/gauge/<int:gauge_id>', methods=['GET'])
def read_gauge_by_id(gauge_id):
    """ GET request to /api/gauge/<gauge_id> will return a Gauge object
        matching the id passed
    """
    session = get_session(current_app)
    gauge = session.query(Gauge).filter(Gauge.id == gauge_id).first()
    if not gauge:
        return error_out(MissingResourceError('Gauge'))
    return jsonify(gauge.shallow_json)


@api_01.route('/gauges/', methods=['GET'])
def read_gauges():
    """ GET request to /api/gauges/ will return a series of Gauge objects """
    session = get_session(current_app)
    gauges = session.query(Gauge).all()
    if not gauges:
        return error_out(MissingResourceError('Gauge'))
    return jsonify([g.shallow_json for g in gauges])


@api_01.route('/gauge/<int:gauge_id>', methods=['PUT'])
def update_gauge(gauge_id):
    """ PUT request to /api/gauge/<gauge_id> will update Gauge object <id>
        with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    gauge = session.query(Gauge).filter(Gauge.id == gauge_id).first()
    if not gauge:
        return error_out(MissingResourceError('Gauge'))
    for k, v in put_data.iteritems():
        setattr(gauge, k, v)
    session.add(gauge)
    session.commit()
    return jsonify(gauge.shallow_json)


@api_01.route('/gauge/<int:gauge_id>', methods=['DELETE'])
def delete_gauge(gauge_id):
    """ DELETE-ing to /api/v1.0/gauge/<gauge_id> will delete the target Gauge
        object from the database
    """
    session = get_session(current_app)
    gauge = session.query(Area).filter(Gauge.id == gauge_id).first()
    if not gauge:
        return jsonify({'Error': 'No gauge found with id {}'.format(gauge_id)}), 404
    session.delete(gauge)
    session.commit()
    return jsonify(201)
