import requests as req
import json
import random

PORT = '80'
API = 'http://0.0.0.0:' + PORT + '/stella/api/v1'


def main():
    r = req.post(API + '/tokens', auth=('participant_a@stella.org', 'pass'))
    r_json = json.loads(r.text)
    token = r_json.get('token')
    r = req.get(API + '/rankings', auth=(token, ''))
    r_json = json.loads(r.text)
    ranking_id = random.choice(r_json.get('rids'))
    r = req.get(API + '/rankings/' + str(ranking_id), auth=(token, ''))
    print(r.text)


if __name__ == '__main__':
    main()
