"""
    River-API Stuff
    ==========================================
    API code is organized into sections based on the resource. Each resource has the following mandatory methods.
    
    Create new instance of resource
    ------------------------------------------
      * URL:        /api/v1.0/resource
      * Method:     POST
      * Route:      create_resource()
      * Returns:    shallow JSON-serialization of successfully-added resource
      * Required:   True
    
    Get Single Resource by numeric identifier
    ------------------------------------------
      * URL:        /api/v1.0/resource/<int:resource_id>
      * Method:     GET
      * Route:      read_resource_by_id(resource_id)
      * Returns:    single JSON-serialized object
      * Required:   True
      
    Get single resource by name string
    ------------------------------------------
      * URL:        /api/v1.0/resource/<string:resource_name>
      * Method:     GET
      * Route:      read_resource_by_name(resource_name)
      * Returns:    full JSON-serialized object
      * Required:   False
      * Note:       This only really applies to things that one may want to look up by name, like River ...
                    top-level items.
    
    Get all resources of a particular type
    ------------------------------------------
      * URL:        /api/v1.0/resources/ 
      * Method:     GET
      * Route:      read_resources()
      * Returns:    array of JSON-serialized objects
      * Required:   True
    
    Update single resource by numeric identifier
    ------------------------------------------
      * URL:        /api/v1.0/resource/<int:resource_id>
      * Method:     PUT
      * Route:      update_resource(resource_id)
      * Returns:    shallow JSON-serialization of successfully-updated resource instance
      * Required:   True
      
    Delete single resource by numeric identifier
    ------------------------------------------
      * URL:        /api/v1.0/resource/<int:resource_id>
      * Method:     DELETE
      * Route:      delete_resource(resource_id)
      * Returns:    200
                    
    Full list of available resources
    ==========================================
    Each resource, along with a brief description, is provided below
    
    River
    Area
    Gauge
    GaugeData
    User
    
"""
from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user
from pymysql.err import IntegrityError
from ... import get_db, get_session
from ... models.rivers import *
from ... models.social import *
from sqlalchemy import desc

api_01 = Blueprint('api_01', __name__, url_prefix='api/v1.0')


# API Routes for accessing and managing river information
# With these API endpoints, users can retrieve river information by id or name,
# retrieve a list of rivers, add new rivers, update existing rivers.
@api_01.route('/river', methods=['POST'])
def create_river():
    """ POSTing to /api/rivers will create a new River object in the database """
    if not request.json:
        return jsonify({'Error': 'You must post JSON to create a new River'}), 400
    session = get_session(current_app)
    river = River(**request.json)
    session.add(river)
    session.commit()
    return jsonify(river.json)


@api_01.route('/river/<int:river_id>', methods=['GET'])
def read_river_by_id(river_id):
    session = get_session(current_app)
    river = session.query(River).filter(River.id == river_id).first()
    return jsonify(river.json)


@api_01.route('/river/<string:river_name>', methods=['GET'])
def read_river_by_name(river_name):
    session = get_session(current_app)
    river = session.query(River).filter(River.name == river_name).first()
    return jsonify(river.json)


@api_01.route('/rivers/', methods=['GET'])
def read_rivers():
    session = get_session(current_app)
    rivers = session.query(River).all()
    return jsonify([river.json for river in rivers])


@api_01.route('/river/<int:river_id>', methods=['PUT'])
def update_river(river_id):
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return jsonify({'Error': "You can't put data without data!"}), 400
    gauge = session.query(River).filter(River.id == river_id).first()
    if not gauge:
        return jsonify({'Error': 'No river found with id {}'.format(river_id)}), 404
    for k, v in put_data.iteritems():
        setattr(gauge, k, v)
    session.add(gauge)
    session.commit()
    return jsonify(gauge.shallow_json)


@api_01.route('/river/<int:river_id>', methods=['DELETE'])
def delete_river(river_id):
    session = get_session(current_app)
    river = session.query(River).filter(River.id == river_id).first()
    if not river:
        return jsonify({'Error': 'No river found with id {}'.format(river_id)}), 404
    session.delete(river)
    session.commit()
    return jsonify(200)


# API Routes for accessing and managing area information
# With these API endpoints, users can retrieve area information by id,
# retrieve a list of areas, add new areas, update existing areas.
@api_01.route('/area', methods=['POST'])
def create_area():
    """ POSTing to /api/v1.0/areas will create a new Area object in the database """
    if not request.json:
        return jsonify({'Error': 'You must post JSON to create a new Area'}), 400
    session = get_session(current_app)
    area = Area(name=request.json['name'])
    session.add(area)
    session.commit()
    return jsonify(area.shallow_json)


@api_01.route('/area/<int:area_id>', methods=['GET'])
def read_area_by_id(area_id):
    session = get_session(current_app)
    area = session.query(Area).filter(Area.id == area_id).first()
    if not area:
        return jsonify({'Error': 'No area found with id {}'.format(area_id)}), 404
    return jsonify(area.shallow_json)


@api_01.route('/areas/', methods=['GET'])
def read_areas():
    session = get_session(current_app)
    areas = session.query(Area).all()
    return jsonify([area.shallow_json for area in areas])


@api_01.route('/area/<int:area_id>', methods=['PUT'])
def update_area(area_id):
    """ PUT request to /api/area/<area_id> will update Area object <id> with fields passed """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return jsonify({'Error': "You can't put data without data!"}), 400
    area = session.query(Area).filter(Area.id == area_id).first()
    if not area:
        return jsonify({'Error': 'No river found with id {}'.format(area_id)}), 404
    for k, v in put_data.iteritems():
        setattr(area, k, v)
    session.add(area)
    session.commit()
    return jsonify(area.shallow_json)


@api_01.route('/area/<int:area_id>', methods=['DELETE'])
def delete_area(area_id):
    """ DELETE-ing to /api/v1.0/area/<area_id> will delete the target Area object from the database """
    session = get_session(current_app)
    area = session.query(Area).filter(Area.id == area_id).first()
    if not area:
        return jsonify({'Error': 'No area found with id {}'.format(area_id)}), 404
    session.delete(area)
    session.commit()
    return jsonify(201)


# API Routes for accessing and managing gauge information
# With these API endpoints, users can retrieve gauge information by id,
# retrieve a list of gauges, add new gauges, update existing gauges.
@api_01.route('/gauge', methods=['POST'])
def create_gauge():
    """ POSTing to /api/gauges will create a new Gauge object in the database """
    session = get_session(current_app)
    gauge = Gauge(**request.json)
    session.add(gauge)
    session.commit()
    session.close()
    return jsonify(gauge.shallow_json)


@api_01.route('/gauge/<int:gauge_id>', methods=['GET'])
def read_gauge_by_id(gauge_id):
    """ GET request to /api/gauge/<gauge_id> will return a Gauge object matching the id passed """
    session = get_session(current_app)
    gauge = session.query(Gauge).filter(Gauge.id == gauge_id).first()
    if not gauge:
        return jsonify({'Error': 'No gauge found with id {}'.format(gauge_id)}), 404
    return jsonify(gauge.shallow_json)


@api_01.route('/gauges/', methods=['GET'])
def read_gauges():
    """ GET request to /api/gauges/ will return a series of Gauge objects -- no filters """
    session = get_session(current_app)
    gauges = session.query(Gauge).all()
    if not gauges:
        return jsonify({'Error': 'No Gauge objects available'}), 404
    return jsonify([g.shallow_json for g in gauges])


@api_01.route('/gauge/<int:gauge_id>', methods=['PUT'])
def update_gauge(gauge_id):
    """ PUT request to /api/gauge/<gauge_id> will update Gauge object <id> with fields passed """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return jsonify({'Error': "You can't put data without data!"}), 400
    gauge = session.query(Gauge).filter(Gauge.id == gauge_id).first()
    if not gauge:
        return jsonify({'Error': 'No gauge found with id {}'.format(gauge_id)}), 404
    for k, v in put_data.iteritems():
        setattr(gauge, k, v)
    session.add(gauge)
    session.commit()
    return jsonify(gauge.shallow_json)


@api_01.route('/gauge/<int:gauge_id>', methods=['DELETE'])
def delete_gauge(gauge_id):
    """ DELETE-ing to /api/v1.0/gauge/<gauge_id> will delete the target Gauge object from the database """
    session = get_session(current_app)
    gauge = session.query(Area).filter(Gauge.id == gauge_id).first()
    if not gauge:
        return jsonify({'Error': 'No gauge found with id {}'.format(gauge_id)}), 404
    session.delete(gauge)
    session.commit()
    return jsonify(201)


# Perhipheral river functionality
# River-related queries that are not pulling the actual river objects
# These are
@api_01.route('/gauge_data/', methods=['POST'])
def create_gauge_data():
    session = get_session(current_app)
    flow = request.json
    if not flow:
        return jsonify({'Error': 'You must post JSON to create a new data-point'}), 405
    gd = GaugeData(**flow)
    session.add(gd)
    try:
        session.commit()
    except:
        return jsonify({'Error': 'You are attempting to add a duplicate datapoint'}), 409
    return jsonify(201)


@api_01.route('/river/<int:river_id>/flow', methods=['GET'])
def check_flow_by_river_id(river_id):
    session = get_session(current_app)
    river = session.query(River).filter(River.id == river_id).first()
    flow = river.current_flow
    json = {'river': river.name, 'timestamp': flow['timestamp'], 'flow': flow['flow']}
    return jsonify(json)



# Social Functionality via API
# The social aspect of this application is centered on the concept of the Trip and PaddleLogEntry
# User objects and Trip objects are the vectors through which we can retrieve Logs
# json properties for both User and Trip will contain a 'logs' field which is an array of serialized
# log objects. Logs can also be retrieved directly by their id value or indirectly by the get_user_logs_by_id()
# route ('/user/<int:user_id>/logs') and get_user_logs_by_alias() route ('/user/<string:alias>/logs')
@api_01.route('/log/<int:entry_id>', methods=['GET'])
def get_log_by_id(entry_id):
    session = get_session(current_app)
    log = session.query(PaddleLogEntry).filter(PaddleLogEntry.id == entry_id).first()
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
        return jsonify({'Error': 'You must post JSON to create a new River'}), 400
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


@api_01.route('/user/<int:user_id>/favorite/<river_id>', methods=['POST'])
def add_favorite_river(user_id, river_id):
    insert = associate_user_favorites.insert().values(
        user_id=user_id,
        river_id=river_id
    )
    con = get_db(current_app)
    con.execute(insert)
    return jsonify(200)
