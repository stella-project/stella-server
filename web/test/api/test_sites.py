import pytest
import json
from base64 import b64encode

from ..create_test_data import create_session, create_feedback


def test_get_site_info_by_name(client, users):
    credentials = b64encode(str.encode(":".join([users["site"].email, "pass"]))).decode(
        "utf-8"
    )
    result = client.get(
        "".join(["/stella/api/v1/sites/", users["site"].username]),
        headers={"Authorization": f"Basic {credentials}"},
    )
    assert result.status_code == 200
    site_info = json.loads(result.data)
    assert site_info.get("id") == users["site"].id


@pytest.mark.parametrize("type", ["ranker", "recommender"])
def test_post_session(client, users, systems, type):
    new_test_session = create_session(type, users, systems)
    credentials = b64encode(str.encode(":".join([users["site"].email, "pass"]))).decode(
        "utf-8"
    )
    result = client.post(
        "/stella/api/v1/sites/" + str(users["site"].id) + "/sessions",
        headers={"Authorization": f"Basic {credentials}"},
        json=new_test_session.serialize,
    )
    assert result.status_code == 200

    session_id = result.json.get("session_id")
    assert isinstance(session_id, int)





@pytest.mark.parametrize("type,idx", [("ranker", 0), ("recommender", 1)])
def test_get_site_sessions(client, users, sessions, type, idx):
    credentials = b64encode(str.encode(":".join([users["site"].email, "pass"]))).decode(
        "utf-8"
    )
    result = client.get(
        "/stella/api/v1/sites/" + str(users["site"].id) + "/sessions",
        headers={"Authorization": f"Basic {credentials}"},
    )
    assert result.status_code == 200
    session_data = json.loads(result.data)

    assert len(session_data) == 2  # one ranking and one recommendation session
    assert session_data[idx].get("id") == sessions[type].id
    
