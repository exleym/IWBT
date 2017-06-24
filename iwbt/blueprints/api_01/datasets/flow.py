from datetime import date
from flask import current_app, jsonify, request
from iwbt import get_session
from iwbt.models.rivers import River
from iwbt.util.api_errors import (DatabaseIntegrityError,
                                  MissingResourceError,
                                  MissingJSONError,
                                  PostValidationError)

from iwbt.blueprints.api_01 import api_01, error_out, verify_required_fields


@api_01.route('/dataset/flow_history/<int:river_id>', methods=['GET'])
def historical_flow(river_id):
    """ Historical flow data is provided at the river level. For each
        river, send a GET request with the river id and any of the
        following optional parameters:
        :param start_date: first date to include in dataset -- defaults
                            to all data.
        :param end_date: last date to include in dataset -- defaults to
                            today
        :param freq: Hourly or Daily -- represented by 'H' or 'D'

    """
    start_date = request.args.get('start_date') or date(2000, 1, 1)
    end_date = request.args.get('end_date') or date.today()
    freq = request.args.get('freq') or 'D'
    session = get_session(current_app)
    river = session.query(River).filter(River.id == river_id).first()
    if not river:
        return error_out(MissingResourceError)
    flow = river.current_flow
    json = {'river': river.name, 'timestamp': flow['timestamp'],
            'flow': flow['flow']}
    return jsonify(json)
