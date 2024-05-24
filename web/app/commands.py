import os
import datetime
import click
from app.extensions import db
from app.models import Role, System, User
from flask.cli import with_appcontext


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
        username="participant_a",
        email=os.environ.get("PARTA_MAIL") or "participant_a@stella-project.org",
        role=participant_role,
        password=os.environ.get("PARTA_PASS") or "pass",
    )

    user_part_b = User(
        username="participant_b",
        email=os.environ.get("PARTB_MAIL") or "participant_b@stella-project.org",
        role=participant_role,
        password=os.environ.get("PARTB_PASS") or "pass",
    )

    user_site_a = User(
        username="GESIS",
        email=os.environ.get("GESIS_MAIL") or "gesis@stella-project.org",
        role=site_role,
        password=os.environ.get("GESIS_PASS") or "pass",
    )

    user_site_b = User(
        username="LIVIVO",
        email=os.environ.get("LIVIVO_MAIL") or "livivo@stella-project.org",
        role=site_role,
        password=os.environ.get("LIVIVO_PASS") or "pass",
    )

    db.session.add_all(
        [
            admin_role,
            participant_role,
            site_role,
            user_admin,
            user_part_a,
            user_part_b,
            user_site_a,
            user_site_b,
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

    gesis_rank_precom_base = System(
        status="running",
        name="gesis_rank_precom_base",
        participant_id=user_site_a.id,
        type="RANK",
        submitted="TREC",
        url="https://github.com/stella-project/gesis_rank_precom_base",
        site=user_site_a.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    gesis_rank_precom = System(
        status="running",
        name="gesis_rank_precom",
        participant_id=user_part_b.id,
        type="RANK",
        submitted="TREC",
        url="https://github.com/stella-project/gesis_rank_precom",
        site=user_site_a.id,
        submission_date=datetime.date(2019, 6, 10),
    )

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

    # livivo demo systems:
    livivo_rank_base = System(
        status="running",
        name="livivo_rank_base",
        participant_id=user_part_a.id,
        type="RANK",
        submitted="DOCKER",
        url="https://github.com/stella-project/livivo_rank_base",
        site=user_site_b.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    livivo_rank_precom = System(
        status="running",
        name="livivo_rank_precom",
        participant_id=user_part_b.id,
        type="RANK",
        submitted="DOCKER",
        url="https://github.com/stella-project/livivo_rank_precom",
        site=user_site_b.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    livivo_rank_pyserini = System(
        status="running",
        name="livivo_rank_pyserini",
        participant_id=user_part_a.id,
        type="RANK",
        submitted="DOCKER",
        url="https://github.com/stella-project/livivo_rank_pyserini",
        site=user_site_b.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    livivo_rec_pyserini = System(
        status="running",
        name="livivo_rec_pyserini",
        participant_id=user_part_a.id,
        type="REC",
        submitted="DOCKER",
        url="https://github.com/stella-project/livivo_rec_pyserini",
        site=user_site_b.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    livivo_rec_pyterrier = System(
        status="running",
        name="livivo_rec_pyterrier",
        participant_id=user_part_b.id,
        type="REC",
        submitted="DOCKER",
        url="https://github.com/stella-project/livivo_rec_pyterrier",
        site=user_site_b.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    livivo_rec_precom = System(
        status="running",
        name="livivo_rec_precom",
        participant_id=user_part_b.id,
        type="REC",
        submitted="TREC",
        url="https://github.com/stella-project/livivo_rec_precom",
        site=user_site_b.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    # dev systems
    livivo_precom = System(
        status="running",
        name="livivo_rank_precom",
        participant_id=user_part_b.id,
        type="RANK",
        submitted="TREC",
        url="https://github.com/stella-project/livivo_rank_precom",
        site=user_site_b.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    livivo_base = System(
        status="running",
        name="livivo_base",
        participant_id=user_site_b.id,
        type="RANK",
        submitted="DOCKER",
        url="https://github.com/stella-project/livivo_rank_base",
        site=user_site_b.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    rank_pyterrier = System(
        status="running",
        name="livivo_rank_pyterrier",
        participant_id=user_part_b.id,
        type="RANK",
        submitted="DOCKER",
        url="https://github.com/stella-project/livivo_rank_pyterrier",
        site=user_site_b.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    rank_pyserini = System(
        status="running",
        name="livivo_rank_pyserini",
        participant_id=user_part_b.id,
        type="RANK",
        submitted="DOCKER",
        url="https://github.com/stella-project/livivo_rank_pyserini",
        site=user_site_b.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    rec_pyterrier = System(
        status="running",
        name="gesis_rec_pyterrier",
        participant_id=user_site_a.id,
        type="REC",
        submitted="DOCKER",
        url="https://github.com/stella-project/gesis_rec_pyterrier",
        site=user_site_a.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    rec_pyserini = System(
        status="running",
        name="gesis_rec_pyserini",
        participant_id=user_part_a.id,
        type="REC",
        submitted="DOCKER",
        url="https://github.com/stella-project/gesis_rec_pyserini",
        site=user_site_a.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    recommender_base_a = System(
        status="running",
        name="gesis_rec_precom",
        participant_id=user_part_a.id,
        type="REC",
        submitted="TREC",
        url="https://github.com/stella-project/gesis_rec_precom",
        site=user_site_a.id,
        submission_date=datetime.date(2019, 6, 10),
    )

    db.session.add_all(
        [
            livivo_base,
            livivo_precom,
            rank_pyserini,
            rank_pyterrier,
            recommender_base_a,
            rec_pyterrier,
            rec_pyserini,
            gesis_rank_pyserini,
            gesis_rank_precom_base,
            gesis_rank_precom,
            gesis_rank_pyserini_base,
            gesis_rec_pyserini,
            livivo_rank_base,
            livivo_rank_precom,
            livivo_rank_pyserini,
            livivo_rec_pyserini,
            livivo_rec_pyterrier,
            livivo_rec_precom,
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
