import requests as req
import json

API = 'http://0.0.0.0:8000/stella/api/v1'


def main():
    r = req.post(API + '/tokens', auth=('participant_a@stella.org', 'pass'))
    r_json = json.loads(r.text)
    token = r_json.get('token')
    session_id = 1
    r = req.get(API + '/sessions/' + str(session_id), auth=(token, ''))
    print(r.text)


if __name__ == '__main__':
    main()
