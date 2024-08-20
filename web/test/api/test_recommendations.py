from ..create_test_data import create_result
from base64 import b64encode
import json


def test_post_recommendation(client, users, sessions, feedback):
    credentials = b64encode(str.encode(":".join([users["site"].email, "pass"]))).decode(
        "utf-8"
    )
    result_obj = create_result(sessions, type="recommender")
    result = {
        "q": result_obj.q,
        "q_date": result_obj.q_date,
        "q_time": result_obj.q_time,
        "num_found": result_obj.num_found,
        "page": result_obj.page,
        "rpp": result_obj.rpp,
        "items": result_obj.items,
    }

    rv = client.post(
        "/stella/api/v1/feedbacks/"
        + str(feedback["recommender"][0].id)
        + "/recommendations",
        headers={"Authorization": f"Basic {credentials}"},
        data=result,
    )
    assert 200 == rv.status_code
    print(rv.json)
    assert isinstance(rv.json.get("recommendation_id"), int)


def test_post_recommendation_unauthorized(client, users, sessions, feedback):
    credentials = b64encode(
        str.encode(":".join([users["admin"].email, "pass"]))
    ).decode("utf-8")
    rv = client.post(
        "/stella/api/v1/feedbacks/"
        + str(feedback["recommender"][0].id)
        + "/recommendations",
        headers={"Authorization": f"Basic {credentials}"},
        data={},
    )
    assert 401 == rv.status_code


def test_recommendation_get(client, users, sessions):
    credentials = b64encode(
        str.encode(":".join([users["participant"].email, "pass"]))
    ).decode("utf-8")

    r = client.get(
        "/stella/api/v1/recommendations/" + str(sessions["recommender"].id),
        headers={"Authorization": f"Basic {credentials}"},
    )
    print(sessions["recommender"].id)
    print(r.json)
    assert 200 == r.status_code
    assert r.json["id"] == sessions["recommender"].id


def test_recommendation_get_not_found(client, users, sessions):
    credentials = b64encode(
        str.encode(":".join([users["participant"].email, "pass"]))
    ).decode("utf-8")

    r = client.get(
        "/stella/api/v1/recommendations/" + str("not an id"),
        headers={"Authorization": f"Basic {credentials}"},
    )
    assert 404 == r.status_code


def test_recommendation_put(client, users, sessions, result):
    modified_recommendation = result["recommender"].serialize
    ranking = json.loads(modified_recommendation["items"])
    ranking["1"] = "doc100"
    modified_recommendation["items"] = json.dumps(ranking)

    credentials = b64encode(
        str.encode(":".join([users["participant"].email, "pass"]))
    ).decode("utf-8")

    r = client.put(
        "/stella/api/v1/recommendations/" + str(result["recommender"].id),
        headers={"Authorization": f"Basic {credentials}"},
        data=modified_recommendation,
    )

    assert 200 == r.status_code
    items = json.loads(r.json["items"])
    assert items["1"] == "doc100"


def test_get_recommendations(client, users, result):
    credentials = b64encode(
        str.encode(":".join([users["participant"].email, "pass"]))
    ).decode("utf-8")

    r = client.get(
        "/stella/api/v1/recommendations",
        headers={"Authorization": f"Basic {credentials}"},
    )

    assert 200 == r.status_code
    assert len(r.json) == 1
    assert isinstance(r.json["rids"][0], int)
    assert r.json["rids"][0] == result["recommender"].id
