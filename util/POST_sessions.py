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

HOST = 'http://0.0.0.0:8000'


def main():

    # post new session
    payload = {
        'site_name': 'Site A',
        'site_user': '123.123.123.123',
        'system_ranking': 'rank_exp_a',
        'system_recommendation': 'rec_exp_a'
               }
    r = req.post(HOST + '/stella/api/v1/sessions', data=payload)
    r_text = json.loads(r.text)
    session_id = r_text.get('session_id')
    print(session_id)

    # post new session
    payload = {
        'site_name': 'Site B',
        'site_user': '321.123.123.123',
        'system_ranking': 'rank_exp_b',
        'system_recommendation': 'rec_exp_b'
               }
    r = req.post(HOST + '/stella/api/v1/sessions', data=payload)
    r_text = json.loads(r.text)
    session_id = r_text.get('session_id')
    print(session_id)

    # post new session
    payload = {
        'site_name': 'Site A',
        'site_user': 'xxx.xxx.xxx.xxx',
        'system_ranking': 'rank_exp_a',
        'system_recommendation': 'rec_exp_b'
               }
    r = req.post(HOST + '/stella/api/v1/sessions', data=payload)
    r_text = json.loads(r.text)
    session_id = r_text.get('session_id')
    print(session_id)


if __name__ == '__main__':
    main()
