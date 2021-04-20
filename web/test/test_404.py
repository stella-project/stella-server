import pytest
from app import create_app, db
from app.util import setup_db

MSG_NOT_FOUND = b'<title>Page Not Found</title>\n'

@pytest.fixture
def client():
    app = create_app('default')
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():

            setup_db(db)
        yield client


def test_nonexistent_page(client):
    rv = client.get('/this/page/does/not/exist')
    assert 404 == rv.status_code
    assert MSG_NOT_FOUND in rv.data