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

HOST = 'http://0.0.0.0:8000'


def main():

    click_dict = {
        "doc1": None,
        "doc11": '2019-11-04T00:08:15',
        "doc2": None,
        "doc12": '2019-11-04T00:06:23',
        "doc3": None,
        "doc13": None,
        "doc4": None,
        "doc14": None,
        "doc5": None,
        "doc15": None,
    }

    # post new session
    payload = {
        'start': '2019-11-04 00:06:23',
        'end': '2019-11-04 00:10:38',
        'interleave': True,
        'clicks': json.dumps(click_dict)
               }

    session_id = 1

    r = req.post(HOST + '/stella/api/v1/sessions/' + str(session_id) + '/feedbacks', data=payload)

    r_text = json.loads(r.text)
    feedback_id = r_text.get('feedback_id')
    print(feedback_id)


if __name__ == '__main__':
    main()
