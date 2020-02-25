import requests as req
import json

API = 'http://0.0.0.0:8000/stella/api/v1'


def main():
    feedback_id = 1
    r = req.get(API + '/feedbacks/' + str(feedback_id))
    print(r.text)


if __name__ == '__main__':
    main()
