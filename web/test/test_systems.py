from base64 import b64encode
import json


CORRECT_MAIL = "livivo@stella-project.org"
CORRECT_PASS = "pass"
SITE = "LIVIVO"


def get_site_info(client, email, password, site):
    credentials = b64encode(str.encode(":".join([email, password]))).decode("utf-8")
    rv = client.get(
        "".join(["/stella/api/v1/sites/", site]),
        headers={"Authorization": f"Basic {credentials}"},
    )
    return json.loads(rv.data)


def get_systems(client, email, password, site_id):
    credentials = b64encode(str.encode(":".join([email, password]))).decode("utf-8")
    rv = client.get(
        "".join(["/stella/api/v1/participants/", str(site_id), "/systems"]),
        headers={"Authorization": f"Basic {credentials}"},
    )
    return json.loads(rv.data)


def test_system(client):
    site_info = get_site_info(client, CORRECT_MAIL, CORRECT_PASS, SITE)
    site_id = site_info.get("id")
    systems = get_systems(client, CORRECT_MAIL, CORRECT_PASS, site_id)

    base_system = list(filter(lambda x: x.get("name") == "livivo_base", systems))
    assert len(base_system) >= 1
    assert base_system[0].get("name") == "livivo_base"
    assert base_system[0].get("type") == "RANK"
