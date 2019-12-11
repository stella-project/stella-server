import requests
import json
from random import randint
from datetime import datetime, timedelta

NUM_SESSION = 30
NUM_RANKING = 150
ADDRESS = 'http://0.0.0.0/stella/api/v1'

for i in range(1, NUM_SESSION):
    url = ADDRESS + '/sessions'
    DATA = json.dumps({'start': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       'end': (datetime.now() + timedelta(hours=randint(1, 9))).strftime('%Y-%m-%d %H:%M:%S')})
    r = requests.post(url, data=DATA)
    print(r.text)


for i in range(1, NUM_RANKING + 1):
    session_id = randint(1, NUM_SESSION + 1)
    url = ADDRESS + '/sessions/' + str(session_id) + '/rankings'

    ranking = {'query': 'text',
               'entities':
                   {'doc1':
                       {'click': 'true'},
                    'doc2':
                       {'click': 'false'},
                    'doc3':
                         {'click': 'true'},
                    'doc4':
                        {'click': 'false'},
                    'doc5':
                        {'click': 'false'},
                    'doc6':
                        {'click': 'false'},
                    'doc7':
                        {'click': 'false'},
                    'doc8':
                        {'click': 'false'},
                    'doc9':
                        {'click': 'false'},
                    'doc10':
                        {'click': 'false'},
                    }
               }

    DATA = json.dumps(ranking)
    r = requests.post(url, data=DATA)
    print(r.text)
