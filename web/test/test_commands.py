import requests

from app.app import db
from app.commands import system_cli, user_cli
from app.models import System, User


def get_system(name):
    return db.session.query(System).filter_by(name=name).first()


def test_register_system_defaults(runner, users):
    result = runner.invoke(
        system_cli,
        ["register", "My_System", "--site", "site", "--participant", "participant"],
    )
    assert result.exit_code == 0, result.output
    system = get_system("my_system")
    assert system is not None
    assert system.type == "RANK"
    assert system.submitted == "DOCKER"
    assert system.status == "submitted"
    assert system.url is None
    assert system.site == users["site"].id
    assert system.participant_id == users["participant"].id


def test_register_system_all_options(runner, users):
    result = runner.invoke(
        system_cli,
        [
            "register",
            "rec_sys",
            "--site", "site@stella-project.org",
            "--participant", "participant@stella-project.org",
            "--type", "recommender",
            "--url", "https://github.com/stella-project/rec_sys",
            "--submitted", "trec",
            "--status", "running",
        ],
    )
    assert result.exit_code == 0, result.output
    system = get_system("rec_sys")
    assert system.type == "REC"
    assert system.submitted == "TREC"
    assert system.status == "running"
    assert system.url == "https://github.com/stella-project/rec_sys"


def test_register_system_duplicate_name(runner, users, systems):
    result = runner.invoke(
        system_cli,
        ["register", "ranker", "--site", "site", "--participant", "participant"],
    )
    assert result.exit_code != 0
    assert "already in use" in result.output


def test_register_system_invalid_name(runner, users):
    result = runner.invoke(
        system_cli,
        ["register", "1bad", "--site", "site", "--participant", "participant"],
    )
    assert result.exit_code != 0
    assert get_system("1bad") is None


def test_register_system_site_must_have_site_role(runner, users):
    result = runner.invoke(
        system_cli,
        ["register", "sys", "--site", "participant", "--participant", "participant"],
    )
    assert result.exit_code != 0
    assert "Site role" in result.output


def test_register_system_unknown_participant(runner, users):
    result = runner.invoke(
        system_cli,
        ["register", "sys", "--site", "site", "--participant", "nobody"],
    )
    assert result.exit_code != 0
    assert "nobody" in result.output


# user register


def get_user(username):
    return db.session.query(User).filter_by(username=username).first()


def test_register_user_defaults_to_participant(runner, roles):
    result = runner.invoke(
        user_cli,
        ["register", "alice", "--email", "Alice@Example.org", "--password", "secret"],
    )
    assert result.exit_code == 0, result.output
    user = get_user("alice")
    assert user.email == "alice@example.org"
    assert user.role.name == "Participant"
    assert user.verify_password("secret")


def test_register_user_with_role(runner, roles):
    result = runner.invoke(
        user_cli,
        ["register", "gesis", "--email", "gesis@example.org", "--role", "site", "--password", "pw"],
    )
    assert result.exit_code == 0, result.output
    assert get_user("gesis").role.name == "Site"


def test_register_user_prompts_for_password(runner, roles):
    result = runner.invoke(
        user_cli,
        ["register", "bob", "--email", "bob@example.org"],
        input="pw\npw\n",
    )
    assert result.exit_code == 0, result.output
    assert get_user("bob").verify_password("pw")


def test_register_user_creates_missing_role(runner):
    result = runner.invoke(
        user_cli,
        ["register", "root", "--email", "root@example.org", "--role", "admin", "--password", "pw"],
    )
    assert result.exit_code == 0, result.output
    assert get_user("root").role.name == "Admin"


def test_register_user_duplicate_email(runner, users):
    result = runner.invoke(
        user_cli,
        ["register", "other", "--email", "SITE@stella-project.org", "--password", "pw"],
    )
    assert result.exit_code != 0
    assert "already registered" in result.output


def test_register_user_duplicate_username(runner, users):
    result = runner.invoke(
        user_cli,
        ["register", "site", "--email", "new@example.org", "--password", "pw"],
    )
    assert result.exit_code != 0
    assert "already in use" in result.output


def test_register_user_invalid_username(runner, roles):
    result = runner.invoke(
        user_cli,
        ["register", "1bad", "--email", "x@example.org", "--password", "pw"],
    )
    assert result.exit_code != 0
    assert get_user("1bad") is None


# system sync


class FakeResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error")


def test_sync_pushes_all_systems(app, runner, systems, monkeypatch):
    app.config["STELLA_APP_ADDRESS"] = ["http://app-a", "http://app-b"]
    calls = []

    def fake_post(url, json, timeout):
        calls.append((url, json))
        return FakeResponse()

    monkeypatch.setattr(requests, "post", fake_post)
    result = runner.invoke(system_cli, ["sync"])

    assert result.exit_code == 0, result.output
    assert [url for url, _ in calls] == [
        "http://app-a/stella/api/v1/systems/update",
        "http://app-b/stella/api/v1/systems/update",
    ]
    pushed = calls[0][1]["systems"]
    assert pushed["ranker"] == {"type": "RANK", "status": "LIVE"}
    assert pushed["recommender"]["type"] == "REC"


def test_sync_reports_failures(app, runner, systems, monkeypatch):
    app.config["STELLA_APP_ADDRESS"] = ["http://down", "http://error", "http://ok"]

    def fake_post(url, json, timeout):
        if "down" in url:
            raise requests.ConnectionError("connection refused")
        return FakeResponse(500 if "error" in url else 200)

    monkeypatch.setattr(requests, "post", fake_post)
    result = runner.invoke(system_cli, ["sync"])

    assert result.exit_code == 1
    assert "Failed http://down: connection refused" in result.output
    assert "Failed http://error: 500 Error" in result.output
    assert "Updated http://ok" in result.output


def test_sync_without_address_configured(app, runner):
    app.config["STELLA_APP_ADDRESS"] = []
    result = runner.invoke(system_cli, ["sync"])
    assert result.exit_code != 0
    assert "STELLA_APP_ADDRESS" in result.output
