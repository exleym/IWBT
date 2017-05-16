from flask import Flask, g
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config
from iwbt.models import Base
from iwbt.models.social import User

login_manager = LoginManager()
bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    login_manager.init_app(app)

    from iwbt.blueprints.api_01.views import api_01
    from iwbt.blueprints.main.views import main
    from iwbt.blueprints.rivers.views import rivers
    from iwbt.blueprints.social.views import social

    app.register_blueprint(rivers, url_prefix='/river')
    app.register_blueprint(social, url_prefix='/user')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(api_01, url_prefix='/api')

    with app.app_context():
        get_db(app)


    @login_manager.user_loader
    def load_user(user_id):
        session = get_session(app)
        return session.query(User).filter(User.id == user_id).first()


    return app


def get_db(app):
    if not hasattr(g, 'dbcon'):
        g.dbcon = connect(app)
    return g.dbcon


def get_session(app):
    Session = sessionmaker(bind=get_db(app))
    return Session()


def connect(app):
    eng = create_engine(app.config['DATABASE_URI'])
    if app.config['CREATE_DB']:
        Base.metadata.create_all(eng)
    return eng