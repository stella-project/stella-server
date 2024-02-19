# Release notes
All notable changes to this project will be documented in this file.


- Update minimal Python version to 3.9
    - Update the `python` version in the `Dockerfile` to `3.9`
    - Canfigure automatic tests in github actions to run on `>3.9`

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

- Rework project structure to use a factory pattern
    - Create a factory at `web/app/app.py`
    - Move the `create_app()` function from `__init__.py` to the factory
    - Move flask extensions into `extensions.py`
    - Add `FLASK_APP` environment variable to point to the factory
    - Move `setup_db()` command from `utils.py` to a flask CLI command at `commands.py`.
    - Remove `stella_server.py` as entrypoint

- Rework the command to run the app in the docker compose file
    - Use `flask run` instead of `python stella_server.py`
    - Use `flask db ...` instead of `python manage.py db ...`
    - Use `flask seed-db` to initially setup the database.


- Add an `entrypoint.sh` to handle the database setup and running the app
    - Add `entrypoint.sh` to the `stella-server` Dockerfile
    - Update the startup command in the docker compose file

- Add a healthcheck to the database docker container to prevent the stella-server crashing if the database is not ready
    - Add a healthcheck to the `stella-db` service in the docker compose file
    - Add a `depends_on` to the `stella-server` service in the docker compose file

