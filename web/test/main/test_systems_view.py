from app.app import db
from app.models import System


def login(client, user):
    return client.post(
        "/auth/login", data={"email": user.email, "password": "pass"}, follow_redirects=True
    )


def submit(client, **data):
    form = {"systemname": "new_sys", "type": "Ranker", "GitHubUrl": "", "submit": "Submit"}
    form.update(data)
    return client.post("/systems", data=form, follow_redirects=True)


def get_system(name):
    return db.session.query(System).filter_by(name=name).first()


def test_participant_registers_system_without_url(client, users):
    login(client, users["participant"])
    response = submit(client, site="site")
    assert response.status_code == 200
    system = get_system("new_sys")
    assert system is not None
    assert system.url is None
    assert system.type == "RANK"
    assert system.submitted == "DOCKER"
    assert system.status == "submitted"
    assert system.site == users["site"].id
    assert system.participant_id == users["participant"].id


def test_participant_registers_recommender_with_url(client, users):
    login(client, users["participant"])
    submit(client, site="site", type="Recommender", GitHubUrl="https://github.com/x/y")
    system = get_system("new_sys")
    assert system.type == "REC"
    assert system.url == "https://github.com/x/y"


def test_site_user_registers_system_for_own_site(client, users):
    # The site dropdown is disabled for Site users, so browsers don't send it.
    login(client, users["site"])
    submit(client)
    system = get_system("new_sys")
    assert system is not None
    assert system.site == users["site"].id
    assert system.participant_id == users["site"].id


def test_name_is_lowercased_and_case_insensitive_duplicate_rejected(client, users, systems):
    login(client, users["participant"])
    response = submit(client, site="site", systemname="Ranker")
    assert b"already in use" in response.data
    assert db.session.query(System).filter_by(name="ranker").count() == 1


def test_update_stella_app_button_flashes_result_per_address(app, client, users, systems, monkeypatch):
    import requests

    app.config["STELLA_APP_ADDRESS"] = ["http://ok", "http://down"]

    class OK:
        def raise_for_status(self):
            pass

    def fake_post(url, json, timeout):
        if "down" in url:
            raise requests.ConnectionError("connection refused")
        return OK()

    monkeypatch.setattr(requests, "post", fake_post)
    login(client, users["admin"])
    response = client.get("/system/update_stella_app", follow_redirects=True)
    assert response.status_code == 200
    assert b"Updated STELLA app at http://ok" in response.data
    assert b"Updating STELLA app at http://down failed" in response.data
