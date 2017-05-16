#!~/bin/anaconda2/envs/iwbt/bin/python2.7

import os
from iwbt import create_app
from iwbt.models.social import User
from flask_script import Manager, Server

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
manager = Manager(app)

manager.add_command('runserver', Server(host='0.0.0.0', port=5000))


@manager.command
def test():
    """ Run the unit tests """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
    manager.run()