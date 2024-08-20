import random
import time
from app.models import Session, Feedback, Result
import datetime
import json


def random_date(start, end, prop, format="%Y-%m-%d %H:%M:%S"):
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


def create_session(type, users, systems):
    session_start_date = random_date(
        "2020-01-01 00:00:00", "2020-12-31 23:59:59", random.random()
    )
    session_start_date = datetime.datetime.strptime(
        session_start_date, "%Y-%m-%d %H:%M:%S"
    )
    session_end_date = session_start_date + datetime.timedelta(
        0, random.randint(10, 3000)
    )

    if type == "ranker":
        test_session = Session(
            start=session_start_date,
            end=session_end_date,
            site_id=users["site"].id,
            site_user=users["site"].id,
            system_ranking=systems["ranker"].id,
            system_recommendation=None,
        )
        return test_session
    elif type == "recommender":
        test_session = Session(
            start=session_start_date,
            end=session_end_date,
            site_id=users["site"].id,
            site_user=users["site"].id,
            system_ranking=None,
            system_recommendation=systems["recommender"].id,
        )
        return test_session
    else:
        raise ValueError(
            f"Invalid type of session: {type}, expected 'ranker' or 'recommender'"
        )


def create_feedback(number_of_feedbacks, sessions, type="ranker"):
    generated_feedbacks = []
    for _ in range(0, number_of_feedbacks):
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
            "10": {"docid": "doc15", "clicked": False, "date": None, "type": "BASE"},
        }

        serp_entries = 10
        num_clicks = random.randint(1, serp_entries)
        rank_clicks = random.sample(range(1, serp_entries + 1), num_clicks)

        for click in rank_clicks:
            click_time_str = random_date(
                sessions[type].start.strftime("%Y-%m-%d %H:%M:%S"),
                sessions[type].end.strftime("%Y-%m-%d %H:%M:%S"),
                random.random(),
            )
            click_time = datetime.datetime.strptime(click_time_str, "%Y-%m-%d %H:%M:%S")
            tmp = click_dict.get(str(click))
            tmp["clicked"] = True
            tmp["date"] = click_time_str
            click_dict[click] = tmp

        generated_feedbacks.append(
            Feedback(
                start=sessions[type].start,
                end=sessions[type].end,
                session_id=sessions[type].id,
                interleave=True,
                clicks=json.dumps(click_dict),
            )
        )
        return generated_feedbacks


def create_result(sessions, type="ranker"):
    return Result(
        session_id=sessions[type].id,
        system_id=sessions[type].system_ranking,
        type="EXP" if type == "ranker" else "REC",
        q="query goes here!",
        q_date=sessions[type].start,
        q_time=300,
        num_found=10,
        page=1,
        rpp=10,
        # hits=10, TODO: error in test: web/test/api/test_rankings.py::test_post_rankings - TypeError: 'hits' is an invalid keyword argument for Result
        items=json.dumps(
            {
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
        ),
    )
