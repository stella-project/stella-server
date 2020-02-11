import requests as req
import json

HOST = 'http://0.0.0.0:8000'


def main():

    session_id = 1
    system_name = ''
    feedback_id = 1
    site_name = ''

    # post new ranking
    payload = {
        'session_id': '',
        'system_id': '',
        'feedback_id': '',
        'site_id': '',
        'part_id': '',
        'type': '',
        'q': '',
        'q_date': '',
        'q_time': '',
        'num_found': '',
        'page': '',
        'rpp': '',
        'items': ''
               }
    r = req.post(HOST + '/stella/api/v1/rankings', data=payload)
    r_text = json.loads(r.text)
    # session_id = r_text.get('session_id')
    # print(session_id)


if __name__ == '__main__':
    main()