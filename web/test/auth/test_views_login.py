def logout(client, email, password):
    client.post(
        "/auth/login", data=dict(email=email, password=password), follow_redirects=True
    )
    return client.get("/auth/logout", follow_redirects=True)


def login(client, email, password):
    return client.post(
        "/auth/login", data=dict(email=email, password=password), follow_redirects=True
    )


def test_correct_login_admin(client, users):
    rv = login(client, users["admin"].email, "pass")
    assert 200 == rv.status_code
    assert b"<h1>Hello, admin! </h1>" in rv.data


def test_correct_logout(client, users):
    rv = logout(client, users["admin"].email, "pass")
    assert 200 == rv.status_code
    assert b"You have been logged out." in rv.data


def test_incorrect_mail(client, users):
    rv = login(client, "INCORRECT_MAIL@email.com", "pass")
    assert 200 == rv.status_code
    assert b"Invalid email or password." in rv.data


def test_incorrect_password(client, users):
    rv = login(client, users["admin"].email, "incorrect")
    assert 200 == rv.status_code
    assert b"Invalid email or password." in rv.data
