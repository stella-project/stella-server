import requests as req
import json

API = 'http://0.0.0.0:8000/stella/api/v1/'


def main():
    r = req.get(API + 'rankings')
    print(r.text)


if __name__ == '__main__':
    main()
