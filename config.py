import os

class Config:
    DATABASE_URI = 'mysql+pymysql://iwbt_admin:wetoodeep42@localhost:3306/iwbt'
    DEBUG = False
    CREATE_DB = False
    SECRET_KEY = 'RipItShredIt'
    WUNDERGROUND_API_KEY = '3fb4ff0cfbe7a369'
    NCDC_TOKEN = 'bvHJcsVnxZyGliDnfrFCAQsuWIPxuOfd'


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