import requests as req
import json
import random

PORT = "80"
PORT = "8000"
API = "http://0.0.0.0:" + PORT + "/stella/api/v1"
API = "http://localhost:" + PORT + "/stella/api/v1"


def main():
    r = req.post(API + "/tokens", auth=("participant_a@stella-project.org", "pass"))
    r_json = json.loads(r.text)
    token = r_json.get("token")
    r = req.get(API + "/feedbacks", auth=(token, ""))
    r_json = json.loads(r.text)
    feedback_ids = [feed.get("feedback_id") for feed in r_json]
    feedback_id = random.choice(feedback_ids)

    r = req.get(API + "/feedbacks/" + str(feedback_id), auth=(token, ""))
    r_json = json.loads(r.text)
    r_json.update({"start": "2020-02-02 20:20:02", "end": None})

    r = req.put(API + "/feedbacks/" + str(feedback_id), data=r_json, auth=(token, ""))


if __name__ == "__main__":
    main()
