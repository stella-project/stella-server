# Release notes
All notable changes to this project will be documented in this file.

## Update in Simulate.py 
Initially, there was issue in the naming of the system, URL and correct auth parameters in the script. Changed the URL port to 8000 and also renamed the systems in the script, this fixed the issue with the simulation script

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



