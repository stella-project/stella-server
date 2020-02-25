import requests as req
import json

'''
rank_exp_a
rank_exp_b
rec_exp_a
rec_exp_b
rank_base_a
rank_base_b
rec_base_a
rec_base_b
'''

API = 'http://0.0.0.0:8000/stella/api/v1'


def main():

    # Post new session for Site A
    site_name = 'Site A'

    r = req.get(API + '/sites/' + site_name)
    r_json = json.loads(r.text)
    site_id = r_json.get('id')
    print('Site identifier: ', site_id)

    payload = {
        'site_user': '123.123.123.123',
        'start': '2020-02-20 20:02:20',
        'end': '2020-02-20 20:02:20',
        'system_ranking': 'rank_exp_a',
        'system_recommendation': 'rec_exp_a'
               }

    r = req.post(API + '/sites/' + str(site_id) + '/sessions', data=payload)
    r_json = json.loads(r.text)
    session_id = r_json.get('session_id')
    print('Session identifier: ', session_id)

    # Post new session for Site B
    site_name = 'Site B'

    r = req.get(API + '/sites/' + site_name)
    r_json = json.loads(r.text)
    site_id = r_json.get('id')
    print('Site identifier: ', site_id)

    payload = {
        'site_user': '321.123.123.123',
        'start': '2020-02-20 20:02:20',
        'end': '2020-02-20 20:02:20',
        'system_ranking': 'rank_exp_b',
        'system_recommendation': 'rec_exp_b'
               }

    r = req.post(API + '/sites/' + str(site_id) + '/sessions', data=payload)
    r_json = json.loads(r.text)
    session_id = r_json.get('session_id')
    print('Session identifier: ', session_id)

    # Post new session for Site A

    site_name = 'Site A'

    r = req.get(API + '/sites/' + site_name)
    r_json = json.loads(r.text)
    site_id = r_json.get('id')
    print('Site identifier: ', site_id)

    payload = {
        'site_user': 'xxx.xxx.xxx.xxx',
        'start': '2020-02-20 20:02:20',
        'end': '2020-02-20 20:02:20',
        'system_ranking': 'rank_exp_a',
        'system_recommendation': 'rec_exp_b'
    }

    r = req.post(API + '/sites/' + str(site_id) + '/sessions', data=payload)
    r_json = json.loads(r.text)
    session_id = r_json.get('session_id')
    print('Session identifier: ', session_id)


if __name__ == '__main__':
    main()
