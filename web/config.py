import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-me'
    AUTOMATOR_GH_KEY = os.environ.get('AUTOMATOR_GH_KEY') or None

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class PostgresConfig(Config):
    DEBUG = False
    POSTGRES_USER = os.environ.get('POSTGRES_USER') or 'postgres'
    POSTGRES_PW = os.environ.get('POSTGRES_PW') or 'change-me'
    POSTGRES_URL = os.environ.get('POSTGRES_URL') or 'db:5432'
    POSTGRES_DB = os.environ.get('POSTGRES_DB') or 'postgres'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
                                                                           pw=POSTGRES_PW,
                                                                           url=POSTGRES_URL,
                                                                           db=POSTGRES_DB)


class DemoConfig(Config):
    DEBUG = False
    POSTGRES_USER = os.environ.get('POSTGRES_USER') or 'postgres'
    POSTGRES_PW = os.environ.get('POSTGRES_PW') or 'change-me'
    POSTGRES_URL = os.environ.get('POSTGRES_URL') or 'db-server:5430'
    POSTGRES_DB = os.environ.get('POSTGRES_DB') or 'postgres'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
                                                                           pw=POSTGRES_PW,
                                                                           url=POSTGRES_URL,
                                                                           db=POSTGRES_DB)


config = {
    'default': DevelopmentConfig,
    'demo': DemoConfig,
    'postgres': PostgresConfig
}
