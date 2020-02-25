import requests as req
import json

API = 'http://0.0.0.0:8000/stella/api/v1'


def main():
    session_id = 1

    r = req.get(API + '/sessions/' + str(session_id))
    print(r.text)


if __name__ == '__main__':
    main()
