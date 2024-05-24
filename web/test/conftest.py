import pytest
from app.app import create_app, db
from app.commands import init_db, seed_db


@pytest.fixture
def client():
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
            seed_db()
        yield client
