import pytest
import json

from app.app import db
from app.commands import seed_db, seed_db_command
from app.models import Role, System, User

SYSTEMS_CONFIG = json.dumps(
    {
        "rank_exp": {"type": "ranker", "url": "https://github.com/stella-project/rank_exp"},
        "rank_base": {"type": "ranker", "base": True},
        "rec_precom": {"type": "recommender", "precomputed": True, "hits_path": "$.hits"},
    }
)

ENV = {
    "ADMIN_USERNAME": "boss",
    "ADMIN_MAIL": "Boss@Example.org",
    "ADMIN_PASS": "admin-pw",
    "SITE_USERNAME": "gesis",
    "SITE_MAIL": "gesis@example.org",
    "SITE_PASS": "site-pw",
    "EXPERIMENTER_USERNAME": "experimenter",
    "EXPERIMENTER_MAIL": "exp@example.org",
    "EXPERIMENTER_PASS": "exp-pw",
    "SYSTEMS_CONFIG": SYSTEMS_CONFIG,
}


def user(username):
    return db.session.query(User).filter_by(username=username).first()


def system(name):
    return db.session.query(System).filter_by(name=name).first()


def test_seed_creates_roles_and_users_from_env():
    seed_db(ENV)
    assert {r.name for r in db.session.query(Role)} == {"Admin", "Participant", "Site"}
    assert user("boss").role.name == "Admin"
    assert user("boss").email == "boss@example.org"
    assert user("boss").verify_password("admin-pw")
    assert user("gesis").role.name == "Site"
    assert user("experimenter").role.name == "Participant"
    assert user("experimenter").verify_password("exp-pw")


def test_seed_registers_systems_from_config():
    seed_db(ENV)
    site, experimenter = user("gesis"), user("experimenter")

    exp = system("rank_exp")
    assert (exp.type, exp.submitted, exp.status) == ("RANK", "DOCKER", "running")
    assert exp.url == "https://github.com/stella-project/rank_exp"
    assert exp.participant_id == experimenter.id
    assert exp.site == site.id

    base = system("rank_base")
    assert base.participant_id == site.id  # baselines belong to the site
    assert base.url is None

    precom = system("rec_precom")
    assert (precom.type, precom.submitted) == ("REC", "TREC")


def test_seed_is_idempotent():
    seed_db(ENV)
    log = seed_db(ENV)
    assert all("skipped" in line for line in log)
    assert db.session.query(User).count() == 3
    assert db.session.query(System).count() == 3


def test_seed_without_systems_config_only_creates_users():
    env = {k: v for k, v in ENV.items() if k != "SYSTEMS_CONFIG"}
    seed_db(env)
    assert db.session.query(User).count() == 3
    assert db.session.query(System).count() == 0


def test_seed_command_rejects_invalid_config_before_writing(runner):
    result = runner.invoke(
        seed_db_command, env={**ENV, "SYSTEMS_CONFIG": '{"bad": {"type": "ranking"}}'}
    )
    assert result.exit_code != 0
    assert "ranker" in result.output
    assert db.session.query(User).count() == 0

    result = runner.invoke(seed_db_command, env={**ENV, "SYSTEMS_CONFIG": "{not json"})
    assert result.exit_code != 0
    assert "not valid JSON" in result.output


def test_seed_command_outputs_log(runner):
    result = runner.invoke(seed_db_command, env=ENV)
    assert result.exit_code == 0, result.output
    assert "Registered Admin 'boss'." in result.output
    assert "Registered baseline ranker 'rank_base'." in result.output


def test_seed_rejects_partially_configured_user():
    env = {k: v for k, v in ENV.items() if k not in ("ADMIN_PASS", "SITE_USERNAME")}
    with pytest.raises(ValueError) as e:
        seed_db(env)
    assert "ADMIN_PASS" in str(e.value)
    assert "SITE_USERNAME" in str(e.value)
    assert db.session.query(Role).count() == 0
    assert db.session.query(User).count() == 0


def test_seed_without_any_variables_only_creates_roles():
    log = seed_db({})
    assert db.session.query(Role).count() == 3
    assert db.session.query(User).count() == 0
    assert len(log) == 3  # one "no variables set" line per user


def test_seed_skips_unconfigured_users():
    env = {k: v for k, v in ENV.items() if not k.startswith("ADMIN_")}
    seed_db(env)
    assert user("boss") is None
    assert user("gesis") is not None
    assert user("experimenter") is not None


def test_seed_uses_existing_owners_when_not_in_env(users):
    # `users` fixture: one Site user ("site") and one Participant ("participant").
    seed_db({"SYSTEMS_CONFIG": SYSTEMS_CONFIG})
    assert system("rank_base").participant_id == users["site"].id
    assert system("rank_exp").participant_id == users["participant"].id
    assert system("rank_exp").site == users["site"].id
    assert db.session.query(User).count() == 3  # nobody new


def test_seed_only_baselines_needs_no_experimenter(roles):
    env = {k: v for k, v in ENV.items() if k.startswith("SITE_")}
    env["SYSTEMS_CONFIG"] = json.dumps({"base_only": {"type": "ranker", "base": True}})
    seed_db(env)
    assert system("base_only").participant_id == user("gesis").id


def test_seed_fails_without_site_user():
    env = {"SYSTEMS_CONFIG": SYSTEMS_CONFIG}
    with pytest.raises(ValueError) as e:
        seed_db(env)
    assert "needs a Site user, but there is no user" in str(e.value)
    assert db.session.query(Role).count() == 0


def test_seed_fails_with_ambiguous_existing_owner(users, roles):
    db.session.add(User(username="site2", email="site2@x.org", role=roles["site"], password="pw"))
    db.session.commit()
    with pytest.raises(ValueError) as e:
        seed_db({"SYSTEMS_CONFIG": SYSTEMS_CONFIG})
    assert "2 users" in str(e.value)
    assert db.session.query(System).count() == 0


def test_seed_with_existing_systems_needs_no_owners(users, systems):
    # All systems already exist, so no owners are required.
    log = seed_db({"SYSTEMS_CONFIG": json.dumps({"ranker": {"type": "ranker"}})})
    assert "System 'ranker' already exists, skipped." in log
