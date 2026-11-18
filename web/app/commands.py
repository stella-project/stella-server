import datetime
import os
import re

import click
from app.extensions import db
from app.models import Role, System, User
from sqlalchemy import or_
from flask.cli import AppGroup, with_appcontext


def init_db():
    """Use this function to setup a database with set of pre-registered users."""
    db.create_all()


def seed_db():
    """Use this function to setup a database with set of pre-registered users."""
    # TODO: Make this more verbose and configurable
    # add ranking systems to database

    admin_role = Role(name="Admin")
    participant_role = Role(name="Participant")
    site_role = Role(name="Site")

    user_admin = User(
        username="stella-admin",
        email=os.environ.get("ADMIN_MAIL") or "admin@stella-project.org",
        role=admin_role,
        password=os.environ.get("ADMIN_PASS") or "pass",
    )

    user_part_a = User(
        username="LIVIVO",
        email=os.environ.get("EXPERIMENTER_MAIL") or "experimenter@stella-project.org",
        role=participant_role,
        password=os.environ.get("EXPERIMENTER_PASS") or "pass",
    )

    user_part_b = User(
        username="GESIS",
        email=os.environ.get("EXPERIMENTER_MAIL_REC")
        or "experimenter_rec@stella-project.org",
        role=participant_role,
        password=os.environ.get("EXPERIMENTER_PASS") or "pass",
    )

    # user_part_b = User(
    #     username="participant_b",
    #     email=os.environ.get("PARTB_MAIL") or "participant_b@stella-project.org",
    #     role=participant_role,
    #     password=os.environ.get("PARTB_PASS") or "pass",
    # )

    user_site_a = User(
        username="site",
        email=os.environ.get("SITE_MAIL") or "site@stella-project.org",
        role=site_role,
        password=os.environ.get("SITE_PASS") or "pass",
    )

    # user_site_b = User(
    #     username="LIVIVO",
    #     email=os.environ.get("LIVIVO_MAIL") or "livivo@stella-project.org",
    #     role=site_role,
    #     password=os.environ.get("LIVIVO_PASS") or "pass",
    # )

    db.session.add_all(
        [
            admin_role,
            participant_role,
            site_role,
            user_admin,
            user_part_a,
            user_part_b,
            user_site_a,
            # user_site_b,
        ]
    )

    db.session.commit()

    # gesis demo systems:
    gesis_rank_pyserini = System(
        status="running",
        name="gesis_rank_pyserini",
        participant_id=user_part_a.id,
        type="RANK",
        submitted="DOCKER",
        url="https://github.com/stella-project/gesis_rank_pyserini",
        site=user_site_a.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    # gesis_rank_precom_base = System(
    #     status="running",
    #     name="gesis_rank_precom_base",
    #     participant_id=user_site_a.id,
    #     type="RANK",
    #     submitted="TREC",
    #     url="https://github.com/stella-project/gesis_rank_precom_base",
    #     site=user_site_a.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    # gesis_rank_precom = System(
    #     status="running",
    #     name="gesis_rank_precom",
    #     participant_id=user_part_b.id,
    #     type="RANK",
    #     submitted="TREC",
    #     url="https://github.com/stella-project/gesis_rank_precom",
    #     site=user_site_a.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    gesis_rank_pyserini_base = System(
        status="running",
        name="gesis_rank_pyserini_base",
        participant_id=user_part_a.id,
        type="RANK",
        submitted="DOCKER",
        url="https://github.com/stella-project/gesis_rank_pyserini_base",
        site=user_site_a.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    gesis_rec_pyserini = System(
        status="running",
        name="gesis_rec_pyserini",
        participant_id=user_part_a.id,
        type="REC",
        submitted="DOCKER",
        url="https://github.com/stella-project/gesis_rec_pyserini",
        site=user_site_a.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    # # livivo demo systems:
    # livivo_rank_base = System(
    #     status="running",
    #     name="livivo_rank_base",
    #     participant_id=user_part_a.id,
    #     type="RANK",
    #     submitted="DOCKER",
    #     url="https://github.com/stella-project/livivo_rank_base",
    #     site=user_site_b.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    # livivo_rank_precom = System(
    #     status="running",
    #     name="livivo_rank_precom",
    #     participant_id=user_part_b.id,
    #     type="RANK",
    #     submitted="DOCKER",
    #     url="https://github.com/stella-project/livivo_rank_precom",
    #     site=user_site_b.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    # livivo_rank_pyserini = System(
    #     status="running",
    #     name="livivo_rank_pyserini",
    #     participant_id=user_part_a.id,
    #     type="RANK",
    #     submitted="DOCKER",
    #     url="https://github.com/stella-project/livivo_rank_pyserini",
    #     site=user_site_b.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    # livivo_rec_pyserini = System(
    #     status="running",
    #     name="livivo_rec_pyserini",
    #     participant_id=user_part_a.id,
    #     type="REC",
    #     submitted="DOCKER",
    #     url="https://github.com/stella-project/livivo_rec_pyserini",
    #     site=user_site_b.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    # livivo_rec_pyterrier = System(
    #     status="running",
    #     name="livivo_rec_pyterrier",
    #     participant_id=user_part_b.id,
    #     type="REC",
    #     submitted="DOCKER",
    #     url="https://github.com/stella-project/livivo_rec_pyterrier",
    #     site=user_site_b.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    # livivo_rec_precom = System(
    #     status="running",
    #     name="livivo_rec_precom",
    #     participant_id=user_part_b.id,
    #     type="REC",
    #     submitted="TREC",
    #     url="https://github.com/stella-project/livivo_rec_precom",
    #     site=user_site_b.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    # # dev systems
    # livivo_precom = System(
    #     status="running",
    #     name="livivo_rank_precom",
    #     participant_id=user_part_b.id,
    #     type="RANK",
    #     submitted="TREC",
    #     url="https://github.com/stella-project/livivo_rank_precom",
    #     site=user_site_b.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    # livivo_base = System(
    #     status="running",
    #     name="livivo_base",
    #     participant_id=user_site_b.id,
    #     type="RANK",
    #     submitted="DOCKER",
    #     url="https://github.com/stella-project/livivo_rank_base",
    #     site=user_site_b.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    # rank_pyterrier = System(
    #     status="running",
    #     name="livivo_rank_pyterrier",
    #     participant_id=user_part_b.id,
    #     type="RANK",
    #     submitted="DOCKER",
    #     url="https://github.com/stella-project/livivo_rank_pyterrier",
    #     site=user_site_b.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    # rank_pyserini = System(
    #     status="running",
    #     name="livivo_rank_pyserini",
    #     participant_id=user_part_b.id,
    #     type="RANK",
    #     submitted="DOCKER",
    #     url="https://github.com/stella-project/livivo_rank_pyserini",
    #     site=user_site_b.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    gesis_rec_pyterrier = System(
        status="running",
        name="gesis_rec_pyterrier",
        participant_id=user_part_a.id,
        type="REC",
        submitted="DOCKER",
        url="https://github.com/stella-project/gesis_rec_pyterrier",
        site=user_site_a.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    # rec_pyserini = System(
    #     status="running",
    #     name="gesis_rec_pyserini",
    #     participant_id=user_part_a.id,
    #     type="REC",
    #     submitted="DOCKER",
    #     url="https://github.com/stella-project/gesis_rec_pyserini",
    #     site=user_site_a.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    # recommender_base_a = System(
    #     status="running",
    #     name="gesis_rec_precom",
    #     participant_id=user_part_a.id,
    #     type="REC",
    #     submitted="TREC",
    #     url="https://github.com/stella-project/gesis_rec_precom",
    #     site=user_site_a.id,
    #     submission_date=datetime.date(2019, 6, 10),
    # )

    db.session.add_all(
        [
            # livivo_base,
            # livivo_precom,
            # rank_pyserini,
            # rank_pyterrier,
            # recommender_base_a,
            # rec_pyterrier,
            # rec_pyserini,
            # gesis_rank_precom_base,
            # gesis_rank_precom,
            gesis_rank_pyserini,
            gesis_rank_pyserini_base,
            gesis_rec_pyserini,
            gesis_rec_pyterrier,
            # livivo_rank_base,
            # livivo_rank_precom,
            # livivo_rank_pyserini,
            # livivo_rec_pyserini,
            # livivo_rec_pyterrier,
            # livivo_rec_precom,
        ]
    )

    db.session.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()


@click.command("seed-db")
@with_appcontext
def seed_db_command():
    seed_db()


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


# Subcommands of an AppGroup run inside the app context automatically.
system_cli = AppGroup("system", help="Manage systems.")


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
