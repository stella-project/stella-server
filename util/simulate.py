import requests as req
import json

NUM_SESSION = 100
PORT = '8000'
API = 'http://0.0.0.0:' + PORT + '/stella/api/v1'

import random
import time
import datetime


def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    source: https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, "%Y-%m-%d %H:%M:%S", prop)


def main():

    r = req.post(API + '/tokens', auth=('participant_a@stella.org', 'pass'))
    r_json = json.loads(r.text)
    token = r_json.get('token')

    sites = ['Site A', 'Site B']
    site_users = ['123.123.123.123', '234.234.234.234', '345.345.345.345',
                  '456.456.456.456', '567.567.567.567', '678.678.678.678',
                  '891.891.891.891', '912.912.912.912']
    # rankers = ['Experimental Ranker A', 'Experimental Ranker B', 'Baseline Ranker A', 'Baseline Ranker B']
    rankers = ['Experimental Ranker A', 'Experimental Ranker B']
    # recommenders = ['Experimental Recommender A', 'Experimental Recommender B', 'Baseline Recommender A', 'Baseline Recommender B']
    recommenders = ['Experimental Recommender A', 'Experimental Recommender B']

    for s in range(0, NUM_SESSION):
        session_start = random_date("2020-01-01 00:00:00", "2020-12-31 00:00:00", random.random())
        session_start_date = datetime.datetime.strptime(session_start, "%Y-%m-%d %H:%M:%S")
        session_end_date = session_start_date + datetime.timedelta(0, random.randint(10, 3000))
        site = random.choice(sites)
        site_user = random.choice(site_users)
        ranker = random.choice(rankers)
        recommender = random.choice(recommenders)

        # GET site identifier
        r = req.get(API + '/sites/' + site, auth=(token, ''))
        r_json = json.loads(r.text)
        site_id = r_json.get('id')

        payload = {
            'site_user': site_user,
            'start': session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
            'end': session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
            'system_ranking': ranker,
            'system_recommendation': recommender
        }

        # POST session
        r = req.post(API + '/sites/' + str(site_id) + '/sessions', data=payload, auth=(token, ''))
        r_json = json.loads(r.text)
        session_id = r_json['session_id']

        # POST feedback
        NUM_FEEDBACK = random.randint(0, 4)

        for f in range(0, NUM_FEEDBACK):

            click_dict = {
                "1": {"doc_id": "doc1", "clicked": False, "date": None, "system": "EXP"},
                "2": {"doc_id": "doc14", "clicked": False, "date": None, "system": "BASE"},
                "3": {"doc_id": "doc2", "clicked": False, "date": None, "system": "EXP"},
                "4": {"doc_id": "doc14", "clicked": False, "date": None, "system": "BASE"},
                "5": {"doc_id": "doc3", "clicked": False, "date": None, "system": "EXP"},
                "6": {"doc_id": "doc13", "clicked": False, "date": None, "system": "BASE"},
                "7": {"doc_id": "doc4", "clicked": False, "date": None, "system": "EXP"},
                "8": {"doc_id": "doc14", "clicked": False, "date": None, "system": "BASE"},
                "9": {"doc_id": "doc5", "clicked": False, "date": None, "system": "EXP"},
                "10": {"doc_id": "doc15", "clicked": False, "date": None, "system": "BASE"}
            }

            serp_entries = 10
            num_clicks = random.randint(1, serp_entries)
            rank_clicks = random.sample(range(1, serp_entries + 1), num_clicks)

            for click in rank_clicks:
                click_time_str = random_date(session_start,
                                             session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                                             random.random())
                click_time = datetime.datetime.strptime(click_time_str, "%Y-%m-%d %H:%M:%S")
                tmp = click_dict.get(str(click))
                tmp['clicked'] = True
                tmp['date'] = click_time_str
                click_dict[click] = tmp
                # click_dict.update({click: old})

            payload = {
                'start': session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
                'end': session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                'interleave': True,
                'clicks': json.dumps(click_dict)
            }

            r = req.post(API + '/sessions/' + str(session_id) + '/feedbacks', data=payload, auth=(token, ''))
            r_json = json.loads(r.text)
            feedback_id = r_json['feedback_id']

            r = req.get(API + '/sessions/' + str(session_id) + '/systems', auth=(token, ''))
            r_json = json.loads(r.text)
            ranker_name = r_json.get('RANK')
            print(ranker_name)
            recommender_name = r_json.get('REC')
            print(recommender_name)

            items = {
                "1": "doc1",
                "2": "doc2",
                "3": "doc3",
                "4": "doc4",
                "5": "doc5",
                "6": "doc6",
                "7": "doc7",
                "8": "doc8",
                "9": "doc9",
                "10": "doc10"
            }

            # POST results
            payload = {
                'q': 'query goes here!',
                'q_date': session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
                'q_time': 300,
                'num_found': 10,
                'page': 1,
                'rpp': 10,
                'items': json.dumps(items)
            }

            r = req.post(API + '/feedbacks/' + str(feedback_id) + '/rankings', data=payload, auth=(token, ''))
            print(r.text)


if __name__ == '__main__':
    main()
