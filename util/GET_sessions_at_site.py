import requests as req
import json

PORT = '80'
API = 'http://0.0.0.0:' + PORT + '/stella/api/v1'


def main():
    r = req.post(API + '/tokens', auth=('participant_a@stella.org', 'pass'))
    r_json = json.loads(r.text)
    token = r_json.get('token')
    site_name = 'Site A'
    r = req.get(API + '/sites/' + site_name, auth=(token, ''))
    r_json = json.loads(r.text)
    site_id = r_json.get('id')
    print('Site identifier: ', site_id)
    r = req.get(API + '/sites/' + str(site_id) + '/sessions', auth=(token, ''))
    print(r.text)


if __name__ == '__main__':
    main()
