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

PORT = '80'
API = 'http://0.0.0.0:' + PORT + '/stella/api/v1'


def main():
    r = req.post(API + '/tokens', auth=('participant_a@stella.org', 'pass'))
    r_json = json.loads(r.text)
    token = r_json.get('token')

    # Post new session for Site A
    site_name = 'Site A'

    r = req.get(API + '/sites/' + site_name, auth=(token, ''))
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

    r = req.post(API + '/sites/' + str(site_id) + '/sessions', data=payload, auth=(token, ''))
    r_json = json.loads(r.text)
    session_id = r_json.get('session_id')
    print('Session identifier: ', session_id)

    # Post new session for Site B
    site_name = 'Site B'

    r = req.get(API + '/sites/' + site_name, auth=(token, ''))
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

    r = req.post(API + '/sites/' + str(site_id) + '/sessions', data=payload, auth=(token, ''))
    r_json = json.loads(r.text)
    session_id = r_json.get('session_id')
    print('Session identifier: ', session_id)

    # Post new session for Site A

    site_name = 'Site A'

    r = req.get(API + '/sites/' + site_name, auth=(token, ''))
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

    r = req.post(API + '/sites/' + str(site_id) + '/sessions', data=payload, auth=(token, ''))
    r_json = json.loads(r.text)
    session_id = r_json.get('session_id')
    print('Session identifier: ', session_id)


if __name__ == '__main__':
    main()
