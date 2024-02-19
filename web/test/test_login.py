CORRECT_MAIL = "admin@stella-project.org"
CORRECT_PASS = "pass"
INCORRECT_MAIL = "anonymous@stella-project.org"
MSG_GREETINGS = b"Hello, stella-admin!"
MSG_LOGOUT = b"You have been logged out."
MSG_INVALID = b"Invalid email or password."


def logout(client, email, password):
    client.post(
        "/auth/login", data=dict(email=email, password=password), follow_redirects=True
    )
    return client.get("/auth/logout", follow_redirects=True)


def login(client, email, password):
    return client.post(
        "/auth/login", data=dict(email=email, password=password), follow_redirects=True
    )


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
