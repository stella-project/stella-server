import requests as req
import json

'''
rank_exp_a
rank_exp_b
rec_exp_a
rec_exp_b
rank_base_a
rank_base_b
rec_base_a
rec_base_b
'''

API = 'http://0.0.0.0:8000/stella/api/v1'


def main():
    r = req.post(API + '/tokens', auth=('participant_a@stella.org', 'pass'))
    r_json = json.loads(r.text)
    token = r_json.get('token')

    click_dict = {
        "1": {"doc_id": "doc1", "clicked": False, "date": None, "system": "EXP"},
        "2": {"doc_id": "doc11", "clicked": True, "date": '2019-11-04 00:08:15', "system": "BASE"},
        "3": {"doc_id": "doc2", "clicked": False, "date": None, "system": "EXP"},
        "4": {"doc_id": "doc12", "clicked": True, "date": '2019-11-04 00:06:23', "system": "BASE"},
        "5": {"doc_id": "doc3", "clicked": False, "date": None, "system": "EXP"},
        "6": {"doc_id": "doc13", "clicked": False, "date": None, "system": "BASE"},
        "7": {"doc_id": "doc4", "clicked": False, "date": None, "system": "EXP"},
        "8": {"doc_id": "doc14", "clicked": False, "date": None, "system": "BASE"},
        "9": {"doc_id": "doc5", "clicked": False, "date": None, "system": "EXP"},
        "10": {"doc_id": "doc15", "clicked": False, "date": None, "system": "BASE"}
    }

    # post new session
    payload = {
        'start': '2019-11-04 00:06:23',
        'end': '2019-11-04 00:10:38',
        'interleave': True,
        'clicks': json.dumps(click_dict)
               }

    session_id = 1

    r = req.post(API + '/sessions/' + str(session_id) + '/feedbacks', data=payload, auth=(token, ''))

    r_text = json.loads(r.text)
    feedback_id = r_text.get('feedback_id')
    print(feedback_id)


if __name__ == '__main__':
    main()
