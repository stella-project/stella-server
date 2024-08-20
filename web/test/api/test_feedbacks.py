import json
import pytest
import random
from base64 import b64encode

from ..create_test_data import create_feedback


@pytest.mark.parametrize("type", ["ranker", "recommender"])
def test_post_feedbacks(client, users, sessions, type):
    number_of_feedbacks = random.randint(1, 4)
    feedbacks = create_feedback(number_of_feedbacks, sessions, type)

    credentials = b64encode(str.encode(":".join([users["site"].email, "pass"]))).decode(
        "utf-8"
    )
    for feedback in feedbacks:
        # TODO: The feedback object is serialized to a dictionary here. This could be done in the object itself.
        data = {
            "start": feedback.start,
            "end": feedback.end,
            "interleave": feedback.interleave,
            "clicks": feedback.clicks,
        }
        result = client.post(
            "/stella/api/v1/sessions/" + str(sessions[type].id) + "/feedbacks",
            headers={"Authorization": f"Basic {credentials}"},
            data=data,
        )
        assert 200 == result.status_code
        assert isinstance(result.json.get("feedback_id"), int)


@pytest.mark.parametrize("type", ["ranker", "recommender"])
def test_get_feedbacks(client, users, feedback, sessions, type):
    credentials = b64encode(str.encode(":".join([users["site"].email, "pass"]))).decode(
        "utf-8"
    )
    result = client.get(
        "/stella/api/v1/feedbacks/" + str(feedback[type][0].id),
        headers={"Authorization": f"Basic {credentials}"},
    )
    assert 200 == result.status_code
    assert "clicked" in json.loads(result.json["clicks"])["1"].keys()
    assert "date" in json.loads(result.json["clicks"])["1"].keys()
    assert "type" in json.loads(result.json["clicks"])["1"].keys()

    assert result.json.get("id") == feedback[type][0].id
