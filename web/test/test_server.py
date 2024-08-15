def test_index(client):
    rv = client.get("/")
    assert 200 == rv.status_code
