from ..create_test_data import create_result
from base64 import b64encode


def test_post_rankings(client, users, sessions, feedback):
    credentials = b64encode(str.encode(":".join([users["site"].email, "pass"]))).decode(
        "utf-8"
    )
    result_obj = create_result(sessions)
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
        "/stella/api/v1/feedbacks/" + str(feedback["ranker"][0].id) + "/rankings",
        headers={"Authorization": f"Basic {credentials}"},
        data=result,
    )
    assert 200 == rv.status_code
    assert isinstance(rv.json.get("ranking_id"), int)
