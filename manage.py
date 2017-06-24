#!~/bin/anaconda2/envs/iwbt/bin/python2.7

import os
from data.managers import Busboy, DataSpoofer
from iwbt import create_app, get_db, get_session
from iwbt.models import social, rivers
from flask_script import Manager, Server, Shell, prompt_bool

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
manager = Manager(app)


def _make_context():
    return dict(app=app, rivers=rivers, social=social, get_db=get_db,
                get_session=get_session)


manager.add_command('runserver', Server(host='0.0.0.0', port=5000))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_option('-c', '--config', dest='config', required=False)


@manager.command
def test():
    """ Run the unit tests """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def cleardb():
    if prompt_bool('Are you sure? This will delete all your data (y/n)'):
        busboy = Busboy(app)
        busboy.run()


@manager.command
def dataspoof():
    """ Populate a development database with sample data """
    rivers = 5
    rapids = 5
    data_spoofer = DataSpoofer(app, rivers, rapids)
    data_spoofer.run()




if __name__=='__main__':
    manager.run()
