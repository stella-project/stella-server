from app.app import db
from app.models import User


def test_register_creates_participant(client, roles):
    response = client.post(
        "/auth/register",
        data={
            "email": "New@Example.org",
            "username": "newuser",
            "password": "pw",
            "password2": "pw",
        },
    )
    assert response.status_code == 302
    user = db.session.query(User).filter_by(username="newuser").first()
    assert user.email == "new@example.org"
    assert user.role.name == "Participant"
    assert user.verify_password("pw")
