import os

class Config:
    DATABASE_URI = 'mysql+pymysql://root:Z3pp3l1n@localhost:3306/iwbt'
    DEBUG = False
    CREATE_DB = False
    SECRET_KEY = 'RipItShredIt'


class DevelopmentConfig(Config):
    DATABASE_URI = 'mysql+pymysql://root:Z3pp3l1n@localhost:3306/iwbt'
    DEBUG = True
    CREATE_DB = True


class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True
    CREATE_DB = True


config = {
    'development': DevelopmentConfig,
    'default': Config,
    'testing': TestingConfig
}