# Release notes
All notable changes to this project will be documented in this file.

## Update to Python 3.9 and Flask 3.0
- Update minimal Python version to 3.9
    - Update the `python` version in the `Dockerfile` to `3.9`
    - Canfigure automatic tests in github actions to run on `>3.9`

- Rework project structure to use a factory pattern
    - Create a factory at `web/app/app.py`
    - Move the `create_app()` function from `__init__.py` to the factory
    - Move flask extensions into `extensions.py`
    - Add `FLASK_APP` environment variable to point to the factory
    - Move `setup_db()` command from `utils.py` to a flask CLI command at `commands.py`.
    - Remove `stella_server.py` as entrypoint

- Rework flask_migrate integration
    - remove `manage.py` script. The migration commands are now available through the `flask` command.

- Switch to new FlaskSQLAlchemy query API
    - Use `db.session.query(<Object>)` instead of `<Object>.query`

- Switch from `itsdangerous`to `pyjwt` to support token authentication
    - Remove `itsdangerous` dependency
    - Add `pyjwt` dependency
    - Update the `generate_auth_token()` and `verify_auth_token()` functions in the `User` model.

- Switch from `flask_scripts` to the flask CLI
    - Remove `flask_scripts` dependency
    - Remove `manager.py` script
    - Add `commands.py` to define custom flask CLI commands

- Rework the command to run the app in the docker compose file
    - Use `flask run` instead of `python stella_server.py`
    - Use `flask db ...` instead of `python manage.py db ...`
    - Use `flask seed-db` to initially setup the database.

- Add an `entrypoint.sh` to handle the database setup and running the app
    - Add `entrypoint.sh` to the `stella-server` Dockerfile
    - Update the startup command in the docker compose file

- Add a `wait-for-it.sh` script to wait for the database to be ready before the server initializes the database
    - Add `wait-for-it.sh`
    - Update the entrypoint to use `wait-for-it.sh`

# Release Notes

All notable changes to this project will be documented in this file.

## Update to Python 3.9 and Flask 3.0

### Changes:
- **Update minimal Python version to 3.9**
    - Updated the `python` version in the `Dockerfile` to `3.9`
    - Configured automatic tests in GitHub Actions to run on `>3.9`

- **Rework project structure to use a factory pattern**
    - Created a factory at `web/app/app.py`
    - Moved the `create_app()` function from `__init__.py` to the factory
    - Moved Flask extensions into `extensions.py`
    - Added `FLASK_APP` environment variable to point to the factory
    - Moved `setup_db()` command from `utils.py` to a Flask CLI command at `commands.py`
    - Removed `stella_server.py` as entrypoint

- **Rework Flask-Migrate integration**
    - Removed `manage.py` script. Migration commands are now available through the `flask` command.

- **Switch to new Flask-SQLAlchemy query API**
    - Replaced `<Object>.query` with `db.session.query(<Object>)`

- **Switch from `itsdangerous` to `pyjwt` to support token authentication**
    - Removed `itsdangerous` dependency
    - Added `pyjwt` dependency
    - Updated `generate_auth_token()` and `verify_auth_token()` functions in the `User` model.

- **Switch from `flask_scripts` to Flask CLI**
    - Removed `flask_scripts` dependency
    - Removed `manager.py` script
    - Added `commands.py` to define custom Flask CLI commands

- **Rework the command to run the app in the Docker Compose file**
    - Replaced `python stella_server.py` with `flask run`
    - Replaced `python manage.py db ...` with `flask db ...`
    - Replaced `python manage.py seed-db` with `flask seed-db`

- **Add an `entrypoint.sh` to handle the database setup and run the app**
    - Added `entrypoint.sh` to the `stella-server` Dockerfile
    - Updated the startup command in the Docker Compose file

- **Add a `wait-for-it.sh` script to wait for the database to be ready before the server initializes the database**
    - Added `wait-for-it.sh`
    - Updated the entrypoint to use `wait-for-it.sh`

---

## UI Generalization

### Updates made in `template/systems.html` and `template/administration.html`:

- **Renaming of instances of `LIVIVO` and `GESIS`**
    - All instances of the terms `LIVIVO` and `GESIS` have been renamed to `ranker` and `recommender` to generalize the UI.

### Specific Changes:

1. **In `systems.html`:**
    - Replaced references of `LIVIVO` with `ranker`
    - Replaced references of `GESIS` with `recommender`

2. **In `administration.html`:**
    - Replaced instances of `LIVIVO` with `ranker`
    - Replaced instances of `GESIS` with `recommender`



