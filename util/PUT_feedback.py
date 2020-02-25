import requests as req
import json
import random

API = 'http://0.0.0.0:8000/stella/api/v1'


def main():
    r = req.get(API + '/feedbacks')
    r_json = json.loads(r.text)
    feedback_ids = [feed.get('feedback_id') for feed in r_json]
    feedback_id = random.choice(feedback_ids)

    r = req.get(API + '/feedbacks/' + str(feedback_id))
    r_json = json.loads(r.text)
    r_json.update({'start': '2020-02-02 20:20:02',
                   'end': None})

    r = req.put(API + '/feedbacks/' + str(feedback_id), data=r_json)


if __name__ == '__main__':
    main()
