from flask import url_for


def test_index(client):
    result = client.get("/")
    assert 200 == result.status_code
