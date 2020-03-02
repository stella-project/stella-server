import requests as req
import json

PORT = '80'
API = 'http://0.0.0.0:' + PORT + '/stella/api/v1'


def main():
    r = req.post(API + '/tokens', auth=('participant_a@stella.org', 'pass'))
    r_json = json.loads(r.text)
    token = r_json.get('token')
    participant_id = 3
    r = req.get(API + '/participants/' + str(participant_id) + '/systems', auth=(token, ''))
    print(r.text)


if __name__ == '__main__':
    main()
