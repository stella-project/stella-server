import pytest
from app import create_app, db
from app.util import setup_db

CORRECT_MAIL = "admin@stella-project.org"
CORRECT_PASS = "pass"
INCORRECT_MAIL = "anonymous@stella-project.org"
MSG_GREETINGS = b'Hello, stella-admin!'
MSG_LOGOUT = b'You have been logged out.'
MSG_INVALID = b'Invalid email or password.'


@pytest.fixture
def client():
    app = create_app('default')
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():

            setup_db(db)
        yield client


def logout(client, email, password):
    client.post('/auth/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)
    return client.get('/auth/logout', follow_redirects=True)


def login(client, email, password):
    return client.post('/auth/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def test_correct_login(client):
        rv = login(client, CORRECT_MAIL, CORRECT_PASS)
        assert 200 == rv.status_code
        assert MSG_GREETINGS in rv.data


def test_correct_logout(client):
        rv = logout(client, CORRECT_MAIL, CORRECT_PASS)
        assert 200 == rv.status_code
        assert MSG_LOGOUT in rv.data


def test_incorrect_login(client):
        rv = login(client, INCORRECT_MAIL, CORRECT_PASS)
        assert 200 == rv.status_code
        assert MSG_INVALID in rv.data
