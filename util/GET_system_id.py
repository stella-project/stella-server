import requests as req
import json

PORT = '80'
API = 'http://0.0.0.0:' + PORT + '/stella/api/v1'

def main():
    r = req.post(API + '/tokens', auth=('participant_a@stella.org', 'pass'))
    r_json = json.loads(r.text)
    token = r_json.get('token')
    system_name = 'rank_elastic'

    r = req.get(API + '/system/id/' + str(system_name), auth=(token, ''))
    print(r.text)


if __name__ == '__main__':
    main()
