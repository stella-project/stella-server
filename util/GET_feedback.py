import requests as req
import json

HOST = 'http://0.0.0.0:8000'


def main():
    feedback_id = 1
    r = req.get(HOST + '/stella/api/v1/feedbacks/' + str(feedback_id))
    print(r.text)


if __name__ == '__main__':
    main()
