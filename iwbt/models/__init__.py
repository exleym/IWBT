from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Model(object):

    @property
    def shallow_json(self):
        return {k: v for k, v in self.__dict__.iteritems() if k not in "_sa_instance_state"}