import requests as req
import json
import random
import datetime

API = 'http://0.0.0.0:8000/stella/api/v1'


def main():
    r = req.get(API + '/rankings')
    r_json = json.loads(r.text)
    rids = r_json.get('rids')
    rid = random.choice(rids)

    r = req.get(API + '/rankings/' + str(rid))
    r_json = json.loads(r.text)

    q_date = "2020-02-02 20:20:02"
    q_time = 222

    items = {
        "1": "doc001",
        "2": "doc002",
        "3": "doc003",
        "4": "doc004",
        "5": "doc005",
        "6": "doc006",
        "7": "doc007",
        "8": "doc008",
        "9": "doc009",
        "10": "doc010"
    }

    r_json.update({'q_date': q_date,
                   'q_time': q_time,
                   'items': items})

    r = req.put(API + '/rankings/' + str(rid), data=r_json)
    print('Updated session with id:', str(rid))


if __name__ == '__main__':
    main()
