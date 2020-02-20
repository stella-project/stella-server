import requests as req
import json
import random

API = 'http://0.0.0.0:8000/stella/api/v1/'


def main():
    r = req.get(API + 'rankings')
    r_json = json.loads(r.text)
    ranking_id = random.choice(r_json.get('rids'))

    r = req.get(API + 'rankings/' + str(ranking_id))
    print(r.text)


if __name__ == '__main__':
    main()
