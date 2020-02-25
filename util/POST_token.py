import requests as req
from requests_jwt import JWTAuth
import json
import random

API = 'http://0.0.0.0:8000/stella/api/v1'


def main():
    r = req.post(API + '/tokens', auth=('participant_a@stella.org', 'pass'))
    r_json = json.loads(r.text)
    token = r_json.get('token')
    print('Token: ', token)


if __name__ == '__main__':
    main()
