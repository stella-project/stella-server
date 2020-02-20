import requests as req
import json

API = 'http://0.0.0.0:8000/stella/api/v1/'


def main():
    participant_id = 3
    r = req.get(API + 'participants/' + str(participant_id) + '/systems')
    print(r.text)


if __name__ == '__main__':
    main()
