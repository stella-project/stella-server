import json
from base64 import b64encode
import pytest
import time
import random
import datetime
from app import create_app, db
from app.util import setup_db

CORRECT_MAIL = "gesis@stella-project.org"
CORRECT_PASS = "pass"
SITE = "GESIS"
RECOMMENDERS = ["gesis_rec_pyterrier", "gesis_rec_pyserini", "gesis_rec_precom"]
USERS = [
    "123.123.123.123",
    "234.234.234.234",
    "345.345.345.345",
    "456.456.456.456",
    "567.567.567.567",
    "678.678.678.678",
    "891.891.891.891",
    "912.912.912.912",
]


def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    source: https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    """
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def generate_session(rankers=None, recommenders=None):
    session_start = random_date(
        "2020-01-01 00:00:00", "2020-12-31 23:59:59", random.random()
    )
    session_start_date = datetime.datetime.strptime(session_start, "%Y-%m-%d %H:%M:%S")
    session_end_date = session_start_date + datetime.timedelta(
        0, random.randint(10, 3000)
    )
    site_user = random.choice(USERS)
    ranker = random.choice(rankers) if rankers else None
    recommender = random.choice(recommenders) if recommenders else None

    return {
        "site_user": site_user,
        "start": session_start_date,
        "end": session_end_date,
        "system_ranking": ranker,
        "system_recommendation": recommender,
    }


def random_date(start, end, prop):
    return str_time_prop(start, end, "%Y-%m-%d %H:%M:%S", prop)


def generate_feedback(number_of_feedbacks, session_start_date, session_end_date):
    for f in range(0, number_of_feedbacks):

        click_dict = {
            "1": {"datasetid": "doc1", "clicked": False, "date": None, "type": "EXP"},
            "2": {"datasetid": "doc14", "clicked": False, "date": None, "type": "BASE"},
            "3": {"datasetid": "doc2", "clicked": False, "date": None, "type": "EXP"},
            "4": {"datasetid": "doc14", "clicked": False, "date": None, "type": "BASE"},
            "5": {"datasetid": "doc3", "clicked": False, "date": None, "type": "EXP"},
            "6": {"datasetid": "doc13", "clicked": False, "date": None, "type": "BASE"},
            "7": {"datasetid": "doc4", "clicked": False, "date": None, "type": "EXP"},
            "8": {"datasetid": "doc14", "clicked": False, "date": None, "type": "BASE"},
            "9": {"datasetid": "doc5", "clicked": False, "date": None, "type": "EXP"},
            "10": {
                "datasetid": "doc15",
                "clicked": False,
                "date": None,
                "type": "BASE",
            },
        }

        serp_entries = 10
        num_clicks = random.randint(1, serp_entries)
        rank_clicks = random.sample(range(1, serp_entries + 1), num_clicks)

        for click in rank_clicks:
            click_time_str = random_date(
                session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
                session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                random.random(),
            )
            click_time = datetime.datetime.strptime(click_time_str, "%Y-%m-%d %H:%M:%S")
            tmp = click_dict.get(str(click))
            tmp["clicked"] = True
            tmp["date"] = click_time_str
            click_dict[click] = tmp

        yield {
            "start": session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "end": session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "interleave": True,
            "clicks": json.dumps(click_dict),
        }


def generate_result(session_start_date):
    return {
        "q": "query goes here!",
        "q_date": session_start_date,
        "q_time": 300,
        "num_found": 10,
        "page": 1,
        "rpp": 10,
        "items": json.dumps(
            {
                "1": "doc1",
                "2": "doc2",
                "3": "doc3",
                "4": "doc4",
                "5": "doc5",
                "6": "doc6",
                "7": "doc7",
                "8": "doc8",
                "9": "doc9",
                "10": "doc10",
            }
        ),
    }


@pytest.fixture
def client():
    app = create_app("default")
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            setup_db(db)
        yield client


def get_token(client, email, password):
    credentials = b64encode(str.encode(":".join([email, password]))).decode("utf-8")
    rv = client.post(
        "/stella/api/v1/tokens", headers={"Authorization": f"Basic {credentials}"}
    )
    data = json.loads(rv.data)
    return data.get("token")


def get_site_info(client, email, password, site):
    credentials = b64encode(str.encode(":".join([email, password]))).decode("utf-8")
    rv = client.get(
        "".join(["/stella/api/v1/sites/", site]),
        headers={"Authorization": f"Basic {credentials}"},
    )
    return json.loads(rv.data)


def get_site_info_token(client, token, site):
    token = b64encode(str.encode(":".join([token, ""]))).decode("utf-8")
    rv = client.get(
        "".join(["/stella/api/v1/sites/", site]),
        headers={"Authorization": f"Bearer {token}"},
    )
    return json.loads(rv.data)


def post_session(client, email, password):
    site_info = get_site_info(client, CORRECT_MAIL, CORRECT_PASS, SITE)
    site_id = site_info.get("id")
    session = generate_session(recommenders=RECOMMENDERS)
    credentials = b64encode(str.encode(":".join([email, password]))).decode("utf-8")
    return client.post(
        "/stella/api/v1/sites/" + str(site_id) + "/sessions",
        headers={"Authorization": f"Basic {credentials}"},
        json=session,
    )


def get_session_info(client, email, password, session_id):
    credentials = b64encode(str.encode(":".join([email, password]))).decode("utf-8")
    rv = client.get(
        "".join(["/stella/api/v1/sessions/", str(session_id)]),
        headers={"Authorization": f"Basic {credentials}"},
    )
    return json.loads(rv.data)


def test_token(client):
    token = get_token(client, CORRECT_MAIL, CORRECT_PASS)
    assert token is not None


def test_get_site_id(client):
    site_info = get_site_info(client, CORRECT_MAIL, CORRECT_PASS, SITE)
    assert isinstance(site_info.get("id"), int)
    assert site_info.get("username") == SITE


def test_get_site_id_token(client):
    token = get_token(client, CORRECT_MAIL, CORRECT_PASS)
    site_info = get_site_info_token(client, token, SITE)
    assert isinstance(site_info.get("id"), int)
    assert site_info.get("username") == SITE


def test_post_session(client):
    session_info = post_session(client, CORRECT_MAIL, CORRECT_PASS)
    assert 200 == session_info.status_code
    session_id = session_info.json.get("session_id")
    assert isinstance(session_id, int)


def test_post_feedbacks(client):
    """Test the endpoints:
    - `/sites/<int:id>/sessions` served by `post_session(id)
    - `/sessions/<int:id>/feedbacks` served by `post_feedback(id)`"""
    site_info = get_site_info(client, CORRECT_MAIL, CORRECT_PASS, SITE)
    site_id = site_info.get("id")
    session = generate_session(recommenders=RECOMMENDERS)
    credentials = b64encode(str.encode(":".join([CORRECT_MAIL, CORRECT_PASS]))).decode(
        "utf-8"
    )
    rv = client.post(
        "/stella/api/v1/sites/" + str(site_id) + "/sessions",
        headers={"Authorization": f"Basic {credentials}"},
        json=session,
    )

    session_id = rv.json.get("session_id")
    number_of_feedbacks = random.randint(0, 4)
    feedbacks = generate_feedback(
        number_of_feedbacks, session.get("start"), session.get("end")
    )

    for feedback in feedbacks:
        credentials = b64encode(
            str.encode(":".join([CORRECT_MAIL, CORRECT_PASS]))
        ).decode("utf-8")
        rv = client.post(
            "/stella/api/v1/sessions/" + str(session_id) + "/feedbacks",
            headers={"Authorization": f"Basic {credentials}"},
            data=feedback,
        )
        assert 200 == rv.status_code
        assert isinstance(rv.json.get("feedback_id"), int)


def test_post_results(client):
    """Test the `/feedbacks/<int:id>/recommendations` endpoint served by `post_recommendation(id)`."""
    site_info = get_site_info(client, CORRECT_MAIL, CORRECT_PASS, SITE)
    site_id = site_info.get("id")
    session = generate_session(recommenders=RECOMMENDERS)
    credentials = b64encode(str.encode(":".join([CORRECT_MAIL, CORRECT_PASS]))).decode(
        "utf-8"
    )
    rv = client.post(
        "/stella/api/v1/sites/" + str(site_id) + "/sessions",
        headers={"Authorization": f"Basic {credentials}"},
        data=session,
    )

    session_id = rv.json.get("session_id")
    number_of_feedbacks = random.randint(0, 4)
    feedbacks = generate_feedback(
        number_of_feedbacks, session.get("start"), session.get("end")
    )

    for feedback in feedbacks:

        rv = client.post(
            "/stella/api/v1/sessions/" + str(session_id) + "/feedbacks",
            headers={"Authorization": f"Basic {credentials}"},
            data=feedback,
        )
        feedback_id = rv.json.get("feedback_id")
        pass

        result = generate_result(session.get("start"))
        rv = client.post(
            "/stella/api/v1/feedbacks/" + str(feedback_id) + "/recommendations",
            headers={"Authorization": f"Basic {credentials}"},
            data=result,
        )
        assert 200 == rv.status_code
        assert isinstance(rv.json.get("recommendation_id"), int)


def test_get_recommendations(client):
    """Test the `/recommendations` endpoint served by `get_recommendations`."""
    credentials = b64encode(str.encode(":".join([CORRECT_MAIL, CORRECT_PASS]))).decode(
        "utf-8"
    )
    session = generate_session(recommenders=RECOMMENDERS)

    # put data
    site_info = get_site_info(client, CORRECT_MAIL, CORRECT_PASS, SITE)
    site_id = site_info.get("id")
    rv = client.post(
        "/stella/api/v1/sites/" + str(site_id) + "/sessions",
        headers={"Authorization": f"Basic {credentials}"},
        data=session,
    )

    session_id = rv.json.get("session_id")
    feedbacks = generate_feedback(1, session.get("start"), session.get("end"))

    for feedback in feedbacks:
        rv = client.post(
            "/stella/api/v1/sessions/" + str(session_id) + "/feedbacks",
            headers={"Authorization": f"Basic {credentials}"},
            data=feedback,
        )
        feedback_id = rv.json.get("feedback_id")

        result = generate_result(session.get("start"))
        rv = client.post(
            "/stella/api/v1/feedbacks/" + str(feedback_id) + "/recommendations",
            headers={"Authorization": f"Basic {credentials}"},
            data=result,
        )
    # test
    rv = client.get(
        "/stella/api/v1/recommendations",
        headers={"Authorization": f"Basic {credentials}"},
    )
    assert 200 == rv.status_code, "Status code is not 200"
    assert isinstance(rv.json.get("rids"), list), "Endpoint returned wrong data"
    assert len(rv.json["rids"]) > 0, "No recommendations found"
