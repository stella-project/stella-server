import requests as req
import json

API = 'http://0.0.0.0:8000/stella/api/v1'


def main():

    session_id = 1
    system_name = 'rank_exp_a'
    feedback_id = 1
    site_name = 'Site A'
    part_name = 'Participant A'

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
        "9": "doc10"
    }

    # post new ranking
    payload = {
        'q': 'this is the query text',
        'q_date': '2019-11-04 00:04:00',
        'q_time': None,
        'num_found': 100,
        'page': 1,
        'rpp': 10,
        'items': json.dumps(items)
               }

    r = req.post(API + '/feedbacks/' + str(feedback_id) + '/rankings', data=payload)
    r_text = json.loads(r.text)
    print(r_text)


if __name__ == '__main__':
    main()
