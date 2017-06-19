from flask import current_app, jsonify, request
from iwbt import get_session
from iwbt.models.rivers import *
from iwbt.util.api_errors import (DatabaseIntegrityError,
                                  MissingResourceError,
                                  MissingJSONError,
                                  PostValidationError)

from iwbt.blueprints.api_01 import api_01, error_out, verify_required_fields


# Perhipheral river functionality
# River-related queries that are not pulling the actual river objects
# These are
@api_01.route('/gauge_data/', methods=['POST'])
def create_gauge_data():
    session = get_session(current_app)
    flow = request.json
    if not flow:
        return error_out(MissingJSONError())
    gd = GaugeData(**flow)
    session.add(gd)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    return jsonify(201)


@api_01.route('/river/<int:river_id>/flow', methods=['GET'])
def check_flow_by_river_id(river_id):
    session = get_session(current_app)
    river = session.query(River).filter(River.id == river_id).first()
    flow = river.current_flow
    json = {'river': river.name, 'timestamp': flow['timestamp'],
            'flow': flow['flow']}
    return jsonify(json)
