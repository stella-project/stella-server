import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-do-not-know'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class PostgresConfig(Config):
    DEBUG = True
    POSTGRES_USER = 'postgres'
    POSTGRES_PW = 'change-me'
    POSTGRES_URL = 'localhost:5432'
    POSTGRES_DB = 'postgres'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
                                                                           pw=POSTGRES_PW,
                                                                           url=POSTGRES_URL,
                                                                           db=POSTGRES_DB)

config = {
    'default': DevelopmentConfig,
    'postgres': PostgresConfig
}
