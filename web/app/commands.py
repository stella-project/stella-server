import datetime
import json
import os
import re

import click
import requests
from app.extensions import db
from app.models import Role, System, User
from sqlalchemy import or_
from flask import current_app
from flask.cli import AppGroup, with_appcontext


def init_db():
    """Use this function to setup a database with set of pre-registered users."""
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()


SYSTEM_NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*$")


def register_system(
    name, site, participant, type="RANK", url=None, submitted="DOCKER", status="submitted"
):
    """Register a new system, applying the same rules as the web form.

    `site` and `participant` are usernames or emails. Raises ValueError on invalid input.
    """
    if not SYSTEM_NAME_PATTERN.match(name):
        raise ValueError(
            "System name must start with a letter, and can only include letters, "
            "numbers, underscores (_), hyphens (-), or dots (.)"
        )
    name = name.lower()
    if db.session.query(System).filter_by(name=name).first():
        raise ValueError(f"System name '{name}' already in use.")

    def find_user(identifier):
        return (
            db.session.query(User)
            .filter(or_(User.username == identifier, User.email == identifier.lower()))
            .first()
        )

    site_user = find_user(site)
    if site_user is None or site_user.role is None or site_user.role.name != "Site":
        raise ValueError(f"No user with the Site role found for '{site}'.")

    participant_user = find_user(participant)
    if participant_user is None:
        raise ValueError(f"No user found for participant '{participant}'.")

    system = System(
        status=status,
        name=name,
        participant_id=participant_user.id,
        type=type,
        submitted=submitted,
        url=url or None,
        site=site_user.id,
        submission_date=datetime.date.today(),
    )
    db.session.add(system)
    db.session.commit()
    return system


def push_systems_to_stella_app(timeout=10):
    """Send all systems and their status to every STELLA app in STELLA_APP_ADDRESS.

    Returns a dict mapping each address to None on success or an error message.
    """
    systems = db.session.query(System).all()
    payload = {
        "systems": {
            system.name: {
                "type": system.type,
                "status": "LIVE" if system.status == "running" else "STOPPED",
            }
            for system in systems
        }
    }

    results = {}
    for address in current_app.config["STELLA_APP_ADDRESS"]:
        current_app.logger.info(f"Updating STELLA App at {address} with payload: {payload}")
        try:
            response = requests.post(
                f"{address}/stella/api/v1/systems/update", json=payload, timeout=timeout
            )
            response.raise_for_status()
            results[address] = None
        except requests.RequestException as e:
            current_app.logger.error(f"Updating STELLA App at {address} failed: {e}")
            results[address] = str(e)
    return results


# Subcommands of an AppGroup run inside the app context automatically.
system_cli = AppGroup("system", help="Manage systems.")


@system_cli.command("sync")
def sync_systems_command():
    """Push all systems and their status to the STELLA app(s)."""
    results = push_systems_to_stella_app()
    if not results:
        raise click.ClickException("No STELLA app address configured (STELLA_APP_ADDRESS).")
    for address, error in results.items():
        if error:
            click.echo(f"Failed {address}: {error}", err=True)
        else:
            click.echo(f"Updated {address}")
    if any(results.values()):
        raise click.exceptions.Exit(1)


@system_cli.command("register")
@click.argument("name")
@click.option("--site", required=True, help="Username or email of the site hosting the system.")
@click.option(
    "--participant", required=True, help="Username or email of the user submitting the system."
)
@click.option(
    "--type",
    "system_type",
    type=click.Choice(["ranker", "recommender"], case_sensitive=False),
    default="ranker",
    show_default=True,
)
@click.option("--url", default=None, help="Optional URL of the system (e.g. GitHub repository).")
@click.option(
    "--submitted",
    type=click.Choice(["docker", "trec"], case_sensitive=False),
    default="docker",
    show_default=True,
    help="How the system is submitted.",
)
@click.option(
    "--status",
    type=click.Choice(["submitted", "running"], case_sensitive=False),
    default="submitted",
    show_default=True,
)
def register_system_command(name, site, participant, system_type, url, submitted, status):
    """Register a new system called NAME."""
    try:
        system = register_system(
            name=name,
            site=site,
            participant=participant,
            type="REC" if system_type.lower() == "recommender" else "RANK",
            url=url,
            submitted=submitted.upper(),
            status=status.lower(),
        )
    except ValueError as e:
        raise click.ClickException(str(e))
    click.echo(f"Registered system '{system.name}' (id {system.id}).")


USERNAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_.]*$")
ROLES = ("Admin", "Participant", "Site")


def register_user(username, email, password, role="Participant"):
    """Register a new user, applying the same rules as the registration form.

    The role is created if it does not exist yet. Raises ValueError on invalid input.
    """
    if not USERNAME_PATTERN.match(username) or len(username) > 64:
        raise ValueError(
            "Usernames must start with a letter and have only letters, numbers, dots or underscores."
        )
    email = email.lower()
    if "@" not in email or len(email) > 64:
        raise ValueError(f"Invalid email address '{email}'.")
    if not password:
        raise ValueError("Password must not be empty.")
    if role not in ROLES:
        raise ValueError(f"Role must be one of {', '.join(ROLES)}.")
    if db.session.query(User).filter_by(email=email).first():
        raise ValueError(f"Email '{email}' already registered.")
    if db.session.query(User).filter_by(username=username).first():
        raise ValueError(f"Username '{username}' already in use.")

    role_obj = db.session.query(Role).filter_by(name=role).first()
    if role_obj is None:
        role_obj = Role(name=role)
        db.session.add(role_obj)

    user = User(username=username, email=email, role=role_obj, password=password)
    db.session.add(user)
    db.session.commit()
    return user


user_cli = AppGroup("user", help="Manage users.")


@user_cli.command("register")
@click.argument("username")
@click.option("--email", required=True)
@click.option(
    "--role",
    type=click.Choice([r.lower() for r in ROLES], case_sensitive=False),
    default="participant",
    show_default=True,
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Prompted for if not given.",
)
def register_user_command(username, email, role, password):
    """Register a new user called USERNAME."""
    try:
        user = register_user(
            username=username, email=email, password=password, role=role.capitalize()
        )
    except ValueError as e:
        raise click.ClickException(str(e))
    click.echo(f"Registered {user.role.name} '{user.username}' (id {user.id}).")


# seed-db

# A user is created when <PREFIX>_USERNAME, <PREFIX>_MAIL and <PREFIX>_PASS are all set.
SEED_USERS = (
    # (env var prefix, role)
    ("ADMIN", "Admin"),
    ("SITE", "Site"),
    ("EXPERIMENTER", "Participant"),
)
SEED_USER_FIELDS = ("USERNAME", "MAIL", "PASS")
SYSTEM_TYPES = {"ranker": "RANK", "recommender": "REC"}


def parse_systems_config(raw):
    """Parse a SYSTEMS_CONFIG JSON string in the stella-app format, e.g.

    {"gesis_rank_pyserini": {"type": "ranker", "base": true, "url": "https://..."}}

    Keys used here: `type` (ranker/recommender, required), `base`, `precomputed` and `url`.
    Other keys (e.g. `hits_path`) are only relevant for stella-app and are ignored.
    """
    try:
        config = json.loads(raw or "{}")
    except json.JSONDecodeError as e:
        raise ValueError(f"SYSTEMS_CONFIG is not valid JSON: {e}")
    if not isinstance(config, dict):
        raise ValueError("SYSTEMS_CONFIG must be a JSON object mapping system names to settings.")
    for name, settings in config.items():
        if not SYSTEM_NAME_PATTERN.match(name):
            raise ValueError(f"Invalid system name '{name}' in SYSTEMS_CONFIG.")
        if not isinstance(settings, dict) or settings.get("type") not in SYSTEM_TYPES:
            raise ValueError(
                f"System '{name}' in SYSTEMS_CONFIG needs a type of 'ranker' or 'recommender'."
            )
    return config


def _seed_users_from_env(env):
    """Return {prefix: {field: value}} for every user whose variables are all set.

    Users without any variables are left out; partially configured users raise ValueError.
    """
    configured, incomplete = {}, []
    for prefix, _ in SEED_USERS:
        values = {field: env.get(f"{prefix}_{field}") for field in SEED_USER_FIELDS}
        if all(values.values()):
            configured[prefix] = values
        elif any(values.values()):
            incomplete += [f"{prefix}_{f}" for f, v in values.items() if not v]
    if incomplete:
        raise ValueError(f"Incomplete user configuration, missing: {', '.join(incomplete)}")
    return configured


def _find_owner(prefix, role, env_users):
    """Username of the user that owns seeded systems for `role`.

    Taken from the environment if configured, otherwise the single existing user with that role.
    """
    if prefix in env_users:
        return env_users[prefix]["USERNAME"]
    users = db.session.query(User).join(Role).filter(Role.name == role).all()
    if len(users) == 1:
        return users[0].username
    reason = "no user" if not users else f"{len(users)} users"
    raise ValueError(
        f"SYSTEMS_CONFIG needs a {role} user, but there is {reason} with that role. "
        f"Set {prefix}_USERNAME, {prefix}_MAIL and {prefix}_PASS, "
        f"or create exactly one with `flask user register`."
    )


def seed_db(environ=None):
    """Create the users defined in the environment and the systems in SYSTEMS_CONFIG.

    A user (ADMIN, SITE, EXPERIMENTER) is created only if its _USERNAME, _MAIL and _PASS
    variables are all set. Baseline systems (`"base": true`) belong to the site user, all
    others to the experimenter; if those are not configured in the environment, the single
    existing user with that role is used.
    Existing users and systems are skipped, so this is safe to run repeatedly.
    Returns a list of log lines.
    """
    env = os.environ if environ is None else environ
    log = []

    # Validate everything first so invalid input fails before anything is written.
    env_users = _seed_users_from_env(env)
    systems_config = parse_systems_config(env.get("SYSTEMS_CONFIG"))
    new_systems = {
        name: settings
        for name, settings in systems_config.items()
        if not db.session.query(System).filter_by(name=name.lower()).first()
    }
    site = experimenter = None
    if new_systems:
        site = _find_owner("SITE", "Site", env_users)
    if any(not settings.get("base") for settings in new_systems.values()):
        experimenter = _find_owner("EXPERIMENTER", "Participant", env_users)

    for role in ROLES:
        if not db.session.query(Role).filter_by(name=role).first():
            db.session.add(Role(name=role))
    db.session.commit()

    for prefix, role in SEED_USERS:
        if prefix not in env_users:
            log.append(f"No {prefix}_* variables set, no {role} user created.")
            continue
        username = env_users[prefix]["USERNAME"]
        email = env_users[prefix]["MAIL"].lower()
        existing = (
            db.session.query(User)
            .filter(or_(User.username == username, User.email == email))
            .first()
        )
        if existing:
            log.append(f"User '{existing.username}' already exists, skipped.")
            if prefix == "SITE" and site:
                site = existing.username
            if prefix == "EXPERIMENTER" and experimenter:
                experimenter = existing.username
            continue
        register_user(
            username=username, email=email, password=env_users[prefix]["PASS"], role=role
        )
        log.append(f"Registered {role} '{username}'.")

    for name in systems_config:
        if name not in new_systems:
            log.append(f"System '{name}' already exists, skipped.")
            continue
        settings = new_systems[name]
        base = bool(settings.get("base"))
        register_system(
            name=name,
            site=site,
            participant=site if base else experimenter,
            type=SYSTEM_TYPES[settings["type"]],
            url=settings.get("url"),
            submitted="TREC" if settings.get("precomputed") else "DOCKER",
            status="running",
        )
        log.append(f"Registered {'baseline ' if base else ''}{settings['type']} '{name}'.")

    return log


@click.command("seed-db")
@with_appcontext
def seed_db_command():
    """Create users from ADMIN_*/SITE_*/EXPERIMENTER_* and systems from SYSTEMS_CONFIG."""
    try:
        for line in seed_db():
            click.echo(line)
    except ValueError as e:
        raise click.ClickException(str(e))
