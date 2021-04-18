import json
from base64 import b64encode
import pytest
import time
import random
import datetime
from app import create_app, db
from app.util import setup_db

CORRECT_MAIL = "livivo@stella-project.org"
CORRECT_PASS = "pass"
SITE = 'LIVIVO'
RANKERS = ['livivo_rank_pyserini', 'livivo_rank_pyterrier', 'livivo_rank_precom']
USERS = ['123.123.123.123', '234.234.234.234',
         '345.345.345.345', '456.456.456.456',
         '567.567.567.567', '678.678.678.678',
         '891.891.891.891', '912.912.912.912']


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
    session_start = random_date("2020-01-01 00:00:00", "2020-12-31 23:59:59", random.random())
    session_start_date = datetime.datetime.strptime(session_start, "%Y-%m-%d %H:%M:%S")
    session_end_date = session_start_date + datetime.timedelta(0, random.randint(10, 3000))
    site_user = random.choice(USERS)
    ranker = random.choice(rankers) if rankers else None
    recommender = random.choice(recommenders) if recommenders else None

    return {
        'site_user': site_user,
        'start': session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
        'end': session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
        'system_ranking': ranker,
        'system_recommendation': recommender
    }


def random_date(start, end, prop):
    return str_time_prop(start, end, "%Y-%m-%d %H:%M:%S", prop)


@pytest.fixture
def client():
    app = create_app('default')
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            setup_db(db)
        yield client


def get_token(client, email, password):
    credentials = b64encode(str.encode(':'.join([email, password]))).decode('utf-8')
    rv = client.post("/stella/api/v1/tokens", headers={"Authorization": f"Basic {credentials}"})
    data = json.loads(rv.data)
    return data.get('token')


def post_session(client, email, password):
    site_info = get_site_info(client, CORRECT_MAIL, CORRECT_PASS, SITE)
    site_id = site_info.get('id')
    session = generate_session(rankers=RANKERS)
    credentials = b64encode(str.encode(':'.join([email, password]))).decode('utf-8')
    return client.post('/stella/api/v1/sites/' + str(site_id) + '/sessions',
                       headers={"Authorization": f"Basic {credentials}"},
                       json=session)


def get_site_info(client, email, password, site):
    credentials = b64encode(str.encode(':'.join([email, password]))).decode('utf-8')
    rv = client.get(''.join(['/stella/api/v1/sites/', site]), headers={"Authorization": f"Basic {credentials}"})
    return json.loads(rv.data)


def test_token(client):
    token = get_token(client, CORRECT_MAIL, CORRECT_PASS)
    assert token is not None


def test_get_site_id(client):
    site_info = get_site_info(client, CORRECT_MAIL, CORRECT_PASS, SITE)
    assert isinstance(site_info.get('id'), int)
    assert site_info.get('username') == SITE


def test_post_session(client):
    session_info = post_session(client, CORRECT_MAIL, CORRECT_PASS)
    assert 200 == session_info.status_code
    session_id = session_info.json.get('session_id')
    assert isinstance(session_id, int)