import pytest
from app.app import create_app, db
from app.commands import init_db, seed_db
from app.models import Role, System, User, Session
import datetime
import json
from base64 import b64encode
import random

from .create_test_data import create_session, create_feedback, create_result


@pytest.fixture()
def app():
    # setup flask app
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True

    # setup database
    with app.app_context():
        init_db()
        # seed_db()

    yield app

    # Teardown code, if necessary
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def clean_db_session(app):
    """Ensure that each test has a clean session."""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        options = dict(bind=connection, binds={})
        session = db._make_scoped_session(options=options)
        db.session = session

        yield session

        transaction.rollback()
        connection.close()
        session.remove()


# Data fixtures
@pytest.fixture
def roles():
    admin_role = Role(name="Admin")
    participant_role = Role(name="Participant")
    site_role = Role(name="Site")

    db.session.add_all([admin_role, participant_role, site_role])
    db.session.commit()

    return {
        "admin": admin_role,
        "participant": participant_role,
        "site": site_role,
    }


@pytest.fixture
def users(roles):
    user_admin = User(
        username="admin",
        email="admin@stella-project.org",
        role=roles["admin"],
        password="pass",
    )

    participant = User(
        username="participant",
        email="participant@stella-project.org",
        role=roles["participant"],
        password="pass",
    )

    site = User(
        username="site",
        email="site@stella-project.org",
        role=roles["site"],
        password="pass",
    )

    db.session.add_all([user_admin, participant, site])
    db.session.commit()

    return {
        "admin": user_admin,
        "participant": participant,
        "site": site,
    }


@pytest.fixture
def auth_users(client, users):
    def auth_user(email, password="pass"):
        credentials = b64encode(str.encode(":".join([email, password]))).decode("utf-8")
        response = client.post(
            "/stella/api/v1/tokens", headers={"Authorization": f"Basic {credentials}"}
        )
        return json.loads(response.data)["token"]

    admin = users["admin"]
    admin.token = auth_user(users["admin"].email)
    participant = users["participant"]
    participant.token = auth_user(users["participant"].email)
    site = users["site"]
    site.token = auth_user(users["site"].email)

    return {
        "admin": admin,
        "participant": participant,
        "site": site,
    }


@pytest.fixture
def systems(users):
    ranker = System(
        status="running",
        name="ranker",
        participant_id=users["participant"].id,
        type="RANK",
        submitted="DOCKER",
        url="https://github.com/test_ranker_url",
        site=users["site"].id,
        submission_date=datetime.date(2019, 6, 10),
    )

    recommender = System(
        status="running",
        name="recommender",
        participant_id=users["participant"].id,
        type="REC",
        submitted="DOCKER",
        url="https://github.com/test_recommender_url",
        site=users["site"].id,
        submission_date=datetime.date(2019, 6, 10),
    )

    db.session.add_all([ranker, recommender])
    db.session.commit()

    return {
        "ranker": ranker,
        "recommender": recommender,
    }


@pytest.fixture
def sessions(users, systems):
    ranker_session = create_session("ranker", users, systems)
    recommender_session = create_session("recommender", users, systems)

    db.session.add_all([ranker_session, recommender_session])
    db.session.commit()

    return {
        "ranker": ranker_session,
        "recommender": recommender_session,
    }


@pytest.fixture
def feedback(sessions):
    number_of_feedbacks = random.randint(1, 4)
    feedbacks_ranker = create_feedback(number_of_feedbacks, sessions, type="ranker")
    db.session.add_all(feedbacks_ranker)

    feedbacks_recommender = create_feedback(
        number_of_feedbacks, sessions, type="recommender"
    )
    db.session.add_all(feedbacks_recommender)

    db.session.commit()

    return {
        "ranker": feedbacks_ranker,
        "recommender": feedbacks_recommender,
    }


@pytest.fixture
def result(sessions):
    results_ranker = create_result(sessions, type="ranker")
    db.session.add(results_ranker)

    results_recommender = create_result(sessions, type="recommender")
    db.session.add(results_recommender)
    db.session.commit()

    return {
        "ranker": results_ranker,
        "recommender": results_recommender,
    }
