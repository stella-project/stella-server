from db import *
from util import *
from config import *
import pandas as pd


def system_stats(system_name):

    total_click = 0
    win = 0
    loss = 0
    tie = 0

    system = systems.select(systems.c.name==system_name).execute().first()

    if system_name not in BASELINE_SYSTEMS:
        system_sessions = sessions.select(sessions.c.system_ranking == system.id).execute().fetchall()
        if not len(system_sessions):
            system_sessions = sessions.select(sessions.c.system_recommendation == system.id).execute().fetchall()

    else:
        type = 'RANK' if system_name == 'livivo_base' else 'REC'
        system_ids = [system.id for system in systems.select(systems.c.type == type).execute().fetchall()]
        if type == 'RANK':
            system_sessions = sessions.select(sessions.c.system_ranking.in_(system_ids)).execute().fetchall()
        else:
            system_sessions = sessions.select(sessions.c.system_recommendation.in_(system_ids)).execute().fetchall()

    session_ids = [s.id for s in system_sessions]
    system_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(session_ids)).execute().fetchall()

    for sys_feed in system_feedbacks:
        base_click_cnt = 0
        exp_click_cnt = 0
        for rank, doc in sys_feed.clicks.items():
            if doc.get('type') == 'EXP' and doc.get('clicked'):
                exp_click_cnt += 1
                if system_name not in BASELINE_SYSTEMS:
                    total_click += 1

            if doc.get('type') == 'BASE' and doc.get('clicked'):
                base_click_cnt += 1
                if system_name in BASELINE_SYSTEMS:
                    total_click += 1

        if base_click_cnt == exp_click_cnt and base_click_cnt + exp_click_cnt > 0:
            tie += 1

        if base_click_cnt > exp_click_cnt:
            if system_name not in BASELINE_SYSTEMS:
                loss += 1
            else:
                win += 1

        if base_click_cnt < exp_click_cnt:
            if system_name not in BASELINE_SYSTEMS:
                win += 1
            else:
                loss += 1

    num_sessions = len(system_sessions)
    impressions = len(system_feedbacks)
    outcome = win / (win + loss) if win + loss > 0 else 0
    ctr = total_click / impressions if impressions > 0 else 0

    return {'Win': win,
            'Loss': loss,
            'Tie': tie,
            'Outcome': outcome,
            'Sessions': num_sessions,
            'Impressions': impressions,
            'Clicks': total_click,
            'CTR': ctr}


def main():
    mkdir(RESULT_DIR)
    system_names = [system.name for system in systems.select().execute().fetchall() if system.name not in NOT_PARTICIPATED]
    overall_stats = {system_name: system_stats(system_name) for system_name in system_names}
    pd.DataFrame.from_dict(overall_stats).transpose().to_csv(os.path.join(RESULT_DIR, 'overall_stats.csv'))


if __name__ == '__main__':
    main()
