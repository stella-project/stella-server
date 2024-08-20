import pytest

MSG_NOT_FOUND = b"<title>Page Not Found</title>\n"


def test_nonexistent_page(client):
    rv = client.get("/this/page/does/not/exist")
    assert 404 == rv.status_code
    assert MSG_NOT_FOUND in rv.data
