import json
from base64 import b64encode
import pytest
from app import create_app, db
from app.util import setup_db

CORRECT_MAIL = "livivo@stella-project.org"
CORRECT_PASS = "pass"
SITE = 'LIVIVO'


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