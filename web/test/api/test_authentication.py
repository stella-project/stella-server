import json
from base64 import b64encode


def test_get_token_authorized(client, users):
    users["admin"].email
    credentials = b64encode(
        str.encode(":".join([users["admin"].email, "pass"]))
    ).decode("utf-8")
    response = client.post(
        "/stella/api/v1/tokens", headers={"Authorization": f"Basic {credentials}"}
    )

    assert response.status_code == 200
    data = json.loads(response.data)

    assert data.get("token") is not None
    assert data.get("expiration") == 3600


def test_get_token_unauthorized(client):
    response = client.post("/stella/api/v1/tokens")

    assert response.status_code == 401
    assert response.data == b"Unauthorized Access"


# TODO: test expiration of token


