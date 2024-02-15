import requests as req
import json

PORT = "80"
PORT = "80"
PORT = "8000"
API = "http://0.0.0.0:" + PORT + "/stella/api/v1"
API = "http://localhost:" + PORT + "/stella/api/v1"


def main():
    r = req.post(API + "/tokens", auth=("participant_a@stella-project.org", "pass"))
    r_json = json.loads(r.text)
    token = r_json.get("token")

    session_id = 1
    system_name = "rank_exp_a"
    feedback_id = 1
    site_name = "Site A"
    part_name = "Participant A"

    items = {
        "0": "doc1",
        "1": "doc2",
        "2": "doc3",
        "3": "doc4",
        "4": "doc5",
        "5": "doc6",
        "6": "doc7",
        "7": "doc8",
        "8": "doc9",
        "9": "doc10",
    }

    # post new ranking
    payload = {
        "q": "this is the query text",
        "q_date": "2019-11-04 00:04:00",
        "q_time": None,
        "num_found": 100,
        "page": 1,
        "rpp": 10,
        "items": json.dumps(items),
    }

    r = req.post(
        API + "/feedbacks/" + str(feedback_id) + "/rankings",
        data=payload,
        auth=(token, ""),
    )
    print(r.text)


if __name__ == "__main__":
    main()
