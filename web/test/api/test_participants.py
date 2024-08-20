from base64 import b64encode


def test_get_participant_systems(client, users, systems):
    credentials = b64encode(str.encode(":".join([users["site"].email, "pass"]))).decode(
        "utf-8"
    )

    result = client.get(
        "/stella/api/v1/participants/" + str(users["participant"].id) + "/systems",
        headers={"Authorization": f"Basic {credentials}"},
    )
    assert 200 == result.status_code
    assert len(result.json) == 2
    for system in result.json:
        assert system["participant_id"] == users["participant"].id


def test_get_participant_sessions(client, users, sessions):
    credentials = b64encode(str.encode(":".join([users["site"].email, "pass"]))).decode(
        "utf-8"
    )
    result = client.get(
        "/stella/api/v1/participants/" + str(users["participant"].id) + "/sessions",
        headers={"Authorization": f"Basic {credentials}"},
    )
    assert 200 == result.status_code
    assert len(result.json) == 2

    print(result.json)
    for session in result.json:
        assert int(session["site_user"]) == users["site"].id


