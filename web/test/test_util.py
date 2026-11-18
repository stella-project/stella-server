import datetime

import ruamel.yaml

from app.app import db
from app.models import System
from app.util import create_stella_app_yaml


def add_system(users, name, url):
    system = System(
        status="running",
        name=name,
        participant_id=users["participant"].id,
        type="RANK",
        submitted="DOCKER",
        url=url,
        site=users["site"].id,
        submission_date=datetime.date(2024, 1, 1),
    )
    db.session.add(system)
    db.session.commit()
    return system


def test_stella_app_yaml_builds_from_url_or_local_source(users, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    add_system(users, "remote_sys", "https://github.com/stella-project/remote_sys")
    add_system(users, "local_sys", None)

    create_stella_app_yaml(type="all", token=None)

    with open(tmp_path / "uploads" / "stella-app.yml") as f:
        services = ruamel.yaml.YAML(typ="safe").load(f)["services"]

    assert services["remote_sys"]["build"] == "https://github.com/stella-project/remote_sys.git"
    assert services["local_sys"]["build"] == "./systems/local_sys"
    assert "local_sys" in services["app"]["depends_on"]
