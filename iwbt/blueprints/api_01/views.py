from flask import Blueprint, current_app, jsonify
from iwbt import get_session
from iwbt.models.rivers import *
from iwbt.models.social import *

api_01 = Blueprint('api_01', __name__, url_prefix='api')


@api_01.route('/add_data', methods=['POST'])
def add_data():
    """ This is a utility endpoint for populating development databases with sample data. should be removed 
        before actual deployment """
    session = get_session(current_app)

    # River Data
    area_bre = Area(name='Blue Ridge Escarpment')
    area_cp = Area(name='Cumberland Plateau')

    river_chat = River(name='Chattooga')
    river_chat.area = area_bre

    river_tal = River(name='Tallulah')
    river_tal.area = area_bre

    user_ex = User(alias='exley', first_name='Exley', last_name='McCormick', moderator=True, admin=True)
    user_ex.password = 'wololo'
    session.add(user_ex)

    session.bulk_save_objects([area_bre, area_cp, river_chat, river_tal])
    session.commit()

    return jsonify(200)
