import logging
import os
import sys

from app.api import api as api_blueprint
from app.auth import auth as auth_blueprint
from app.commands import init_db_command, seed_db_command
from app.extensions import bootstrap, db, login_manager, migrate
from app.main import main as main_blueprint
from config import config
from flask import Flask



def create_app():
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    
    config_name = os.getenv("FLASK_CONFIG") or "default"
    print("Create app from:", __name__)
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config[config_name])
    configure_logger(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(api_blueprint, url_prefix="/stella/api/v1")
    return None


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
