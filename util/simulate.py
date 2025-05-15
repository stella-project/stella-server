import requests as req
import json

NUM_SESSION = 100
PORT = "8000"
# API = 'http://0.0.0.0:' + PORT + '/stella/api/v1'
API = "http://127.0.0.1:" + PORT + "/stella/api/v1"

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


def dataset_recommendations(number_of_sessions=NUM_SESSION, print_feedback=False):
    # r = req.post(API + "/tokens", auth=("gesis@stella.org", "pass"))
    r = req.post(API + "/tokens", auth=("site@stella-project.org", "pass"))
    r_json = json.loads(r.text)

    token = r_json.get("token")

    sites = ["GESIS"]
    site_users = [
        "123.123.123.123",
        "234.234.234.234",
        "345.345.345.345",
        "456.456.456.456",
        "567.567.567.567",
        "678.678.678.678",
        "891.891.891.891",
        "912.912.912.912",
    ]

    rankers = ["gesis_rank_pyserini_base"]
    recommenders = ["gesis_rec_pyserini"]

    for s in range(0, number_of_sessions):
        session_start = random_date(
            "2020-01-01 00:00:00", "2020-12-31 00:00:00", random.random()
        )
        session_start_date = datetime.datetime.strptime(
            session_start, "%Y-%m-%d %H:%M:%S"
        )
        session_end_date = session_start_date + datetime.timedelta(
            0, random.randint(10, 3000)
        )
        site = random.choice(sites)
        site_user = random.choice(site_users)
        ranker = random.choice(rankers)
        recommender = random.choice(recommenders)

        # GET site identifier
        r = req.get(API + "/sites/" + site, auth=(token, ""))
        r_json = json.loads(r.text)
        print("WHAT ARE WE PUTTING IN AS SITE ID",r.text)
        site_id = r_json.get("id")

        payload = {
            "site_user": site_user,
            "start": session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "end": session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "ranker":ranker,
            "system_recommendation": recommender,
        }
        print("this is the payload will help u with ",payload)
        print(API)
        # POST session
        r = req.post(
            "http://127.0.0.1:8000/stella/api/v1" + "/sites/" + str(site_id) + "/sessions", json=payload, auth=(token, "")
        )
        print("THIIIIIIISSSSSSSSSSS S",r)
        r_json = json.loads(r.text)
        print("THIS TEST IN DATASETS RECC",r_json)
        session_id = r_json["session_id"]

        # POST feedback
        number_of_feedbacks = random.randint(0, 4)

        for f in range(0, number_of_feedbacks):
            click_dict = {
                str(i + 1): {
                    "docid": f"doc{i + 1}",
                    "clicked": i % 2 == 0,
                    "date": random_date(
                        session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
                        session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                        random.random()
                        ),
                    "type": "EXP" if i % 2 == 0 else "BASE"
                    }
                for i in range(10)
                }


            serp_entries = 10
            num_clicks = random.randint(1, serp_entries)
            rank_clicks = random.sample(range(1, serp_entries + 1), num_clicks)
            
            

            for click in rank_clicks:
                click_time_str = random_date(
                    session_start,
                    session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                    random.random(),
                )
                click_time = datetime.datetime.strptime(
                    click_time_str, "%Y-%m-%d %H:%M:%S"
                )
                tmp = click_dict.get(str(click))
                if tmp is not None:
                    tmp["clicked"] = True
                    tmp["date"] = click_time_str
                    click_dict[str(click)] = tmp
                else:
                    print(f"WARNING: click_dict missing key: {click}")
                

                # click_dict.update({click: old})

            payload = {
                "start": session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
                "end": session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                "interleave": "true",
                "clicks":  json.dumps(click_dict),
            }
            print("MAKE SURE CLICK IS NOT NONE!!!!!!!!",payload)
            print("clicks type:", type(payload["clicks"]))
            print("Payload:", json.dumps(payload, indent=2))
            print(session_id)
            r = req.post(
                API + "/sessions/"+ str(session_id)+"/feedbacks",
                json=payload,
                auth=(token, ""),
            )
            print(">>>>>>>>>",r)
            r_json = json.loads(r.text)
            print("POST /feedbacks response body:", r.text)
            print(r_json)
            feedback_id = r_json["feedback_id"]
            
            print(r_json)

            r = req.get(
                API + "/sessions/" + str(session_id) + "/systems", auth=(token, "")
            )
            r_json = json.loads(r.text)
            ranker_name = r_json.get("RANK")

            if print_feedback:
                print(ranker_name)

            recommender_name = r_json.get("REC")

            if print_feedback:
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
                "10": "doc10",
            }

            # POST results
            payload = {
                "q": "query goes here!",
                "q_date": session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
                "q_time": 300,
                "num_found": 10,
                "page": 1,
                "rpp": 10,
                "items": items,
            }

            r = req.post(
                API + "/feedbacks/" + str(session_id) + "/recommendations",
                json=payload,
                auth=(token, ""),
            )

            if print_feedback:
                print(r.text)


def rankings(number_of_sessions=NUM_SESSION, print_feedback=False):
    #api
    r = req.post(API + "/tokens", auth=("site@stella-project.org", "pass")) 
    print('THIS IS TEST',r)
    r_json = json.loads(r.text)
    token = r_json.get("token")
    print(">>>> >>>>>>>token is ",token)

    sites = ["GESIS"]
    site_users = [
        "123.123.123.123",
        "234.234.234.234",
        "345.345.345.345",
        "456.456.456.456",
        "567.567.567.567",
        "678.678.678.678",
        "891.891.891.891",
        "912.912.912.912",
    ]

    rankers = ["gesis_rank_pyserini_base",]
    recommenders = ["gesis_rec_pyserini"]

    for s in range(0, number_of_sessions):
        session_start = random_date(
            "2020-01-01 00:00:00", "2020-12-31 00:00:00", random.random()
        )
        print(session_start)
        session_start_date = datetime.datetime.strptime(
            session_start, "%Y-%m-%d %H:%M:%S"
        )
        session_end_date = session_start_date + datetime.timedelta(
            0, random.randint(10, 3000)
        )
        site = random.choice(sites)
        site_user = random.choice(site_users)
        ranker = random.choice(rankers)
        recommender = random.choice(recommenders)

        # GET site identifier
        r = req.get(API + "/sites/" + site, auth=(token, ""))
        print("THIS IS TESTING:::::",r.status_code)
        r_json = json.loads(r.text)
        site_id = r_json.get("id")
        print(">>SITE ID " ,site_id)

        payload = {
            "site_user": site_user,
            "start": session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "end": session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "system_ranking": ranker,
        }

        headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
        r = req.post(
    API + "/sites/" + str(site_id) + "/sessions",
    data=json.dumps(payload),
    headers={"Content-Type": "application/json"},
    auth=req.auth.HTTPBasicAuth("site@stella-project.org", "pass")
)
        # POST session
    
        print("THIS IS TEST ",r.text)
        print("THIS IS TEST ",r_json)
        
        if r.status_code != 200:
            print("ERROR:", r.status_code)
            print("RESPONSE TEXT:", r.text)
            print("REQUEST PAYLOAD:", payload)
            raise Exception("Failed to create session")
        
        temp=r.json()
        print(">>>>>>>>>>>>This is test",r_json)
        session_id = temp.get("session_id")
        print("the session id is again here!!!!!!!!!!!!!!!!!!!!!",session_id)

        # POST feedback
        number_of_feedbacks = random.randint(0, 4)

        for f in range(0, number_of_feedbacks):
            click_dict = {
                "1": {"docid": "doc1", "clicked": False, "date": None, "type": "EXP"},
                "2": {"docid": "doc14", "clicked": False, "date": None, "type": "BASE"},
                "3": {"docid": "doc2", "clicked": False, "date": None, "type": "EXP"},
                "4": {"docid": "doc14", "clicked": False, "date": None, "type": "BASE"},
                "5": {"docid": "doc3", "clicked": False, "date": None, "type": "EXP"},
                "6": {"docid": "doc13", "clicked": False, "date": None, "type": "BASE"},
                "7": {"docid": "doc4", "clicked": False, "date": None, "type": "EXP"},
                "8": {"docid": "doc14", "clicked": False, "date": None, "type": "BASE"},
                "9": {"docid": "doc5", "clicked": False, "date": None, "type": "EXP"},
                "10": {
                    "docid": "doc15",
                    "clicked": False,
                    "date": None,
                    "type": "BASE",
                },
            }

            serp_entries = 10
            num_clicks = random.randint(1, serp_entries)
            rank_clicks = random.sample(range(1, serp_entries + 1), num_clicks)

            for click in rank_clicks:
                click_time_str = random_date(
                    session_start,
                    session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                    random.random(),
                )
                click_time = datetime.datetime.strptime(
                    click_time_str, "%Y-%m-%d %H:%M:%S"
                )
                click_key = str(click)
                tmp = click_dict.get(click_key)
                if tmp:  # only update if it exists
                    tmp["clicked"] = True
                    tmp["date"] = click_time_str
                    click_dict[click_key] = tmp

            payload = {
                "start": session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
                "end": session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                "interleave": True,
                "clicks": json.dumps(click_dict),
            }
            print("Sending payload to /feedbacks:", json.dumps(payload, indent=2))

            # r = req.post(
            #     API + "/sessions/" + str(session_id) + "/feedbacks",
            #     data=payload,
            #     auth=(token, ""),
            # )
            print(">>>>>>>>>>>>",r)
            r_json = json.loads(r.text)
            feedback_id = r_json["session_id"]
    
            # r = req.get(
            #     API + "/sessions/" + str(session_id) + "/systems", auth=(token, "")
            # )
            print( "sfasfdadfa", r.status_code)
            r_json = json.loads(r.text)
            ranker_name = r_json.get("RANK")

            if print_feedback:
                print(ranker_name)

            recommender_name = r_json.get("REC")

            if print_feedback:
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
                "10": "doc10",
            }

            # POST results
            payload = {
                "q": "query goes here!",
                "q_date": session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
                "q_time": 300,
                "num_found": 10,
                "page": 1,
                "rpp": 10,
                "items": json.dumps(items),
            }

            r = req.post(
                API + "/feedbacks/" + str(session_id) + "/rankings",
                data=payload,
                auth=(token, ""),
            )

            if print_feedback:
                print(r.text)


def main():
    dataset_recommendations()


if __name__ == "__main__":
    main()
