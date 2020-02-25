import requests as req
import json


API = 'http://0.0.0.0:8000/stella/api/v1'


def main():
    site_name = 'Site A'
    r = req.get(API + '/sites/' + site_name)
    r_json = json.loads(r.text)
    site_id = r_json.get('id')
    print('Site identifier: ', site_id)

    # Endpoint is not implemented.
    r = req.get(API + '/sites/' + str(site_id) + '/sessions')
    r_json = json.loads(r.text)
    print(r_json)


if __name__ == '__main__':
    main()
