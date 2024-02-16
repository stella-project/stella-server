import pytest

from app.app import create_app, db
from app.util import setup_db


@pytest.fixture
def client():
    app = create_app("default")

    with app.test_client() as client:
        with app.app_context():
            setup_db(db)
        yield client


def test_index(client):
    rv = client.get("/")
    assert 200 == rv.status_code
