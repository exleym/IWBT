"""
    River-API Stuff
    ==========================================
    API code is organized into sections based on the resource. Each resource
    has the following mandatory methods.

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
      * Note:       This only really applies to things that one may want to
                    look up by name, like River ...
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
      * Returns:    shallow JSON-serialization of successfully-updated
                    resource instance
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
from flask import Blueprint

api_01 = Blueprint('api_01', __name__, url_prefix='api/v1.0')


def verify(json, required_fields, allowed_fields=None):
    if not allowed_fields:
        allowed_fields = []
    allowed_fields += required_fields
    passes_required = verify_required_fields(json, required_fields)
    passes_allowed = verify_allowed_fields(json, allowed_fields)
    return passes_required * passes_allowed


def verify_required_fields(json, expected_fields):
    for field in expected_fields:
        try:
            assert field in json
        except AssertionError:
            return False
    return True


def verify_allowed_fields(json, allowed_fields):
    """ Ensure that no fields are passed that are not permitted for a
        given resource.
        :param json: dictionary of POST data passed in request
        :param allowed_fields: list of strings of acceptable parameters
        :return: True if all parameters are allowed; else False
    """
    for k in json.keys():
        if k not in allowed_fields:
            return False
    return True


def error_out(error):
    return error.json_response(True)


from . resources.areas import (create_area, read_area_by_id, read_areas,
                               update_area, delete_area)
from . resources.flow import (create_gauge_data, check_flow_by_river_id)
from . resources.gauges import (create_gauge, read_gauge_by_id, read_gauges,
                                update_gauge, delete_gauge)
from . resources.rivers import (create_river, read_river_by_id,
                                read_river_by_name, read_rivers, update_river,
                                delete_river)
from . resources.sections import (create_section)
from . resources.users import (get_log_by_id, get_user_by_id,
                               get_user_by_alias, get_user_logs_by_id,
                               get_user_logs_by_alias, add_log_entry,
                               add_favorite_river)
