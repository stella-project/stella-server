from db import *
from util import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

RESULT_DIR = 'results'
FILENAME = 'livivo_click_distribution.pdf'
NOT_PARTICIPATED = ['livivo_rank_pyterrier', 'lemuren_elk_docker', 'livivo_rank_precom']


def livivo_click_distribution(feedbacks, type='EXP'):
    click_distr = dict.fromkeys(['title',
                                 'details',
                                 'fulltext',
                                 'order',
                                 'bookmark',
                                 'more_links',
                                 'instock'])

    for feedback in feedbacks:
        livivo_clicks = [rf.get('livivo_clicks') for rf in feedback.clicks.values() if rf.get('type') == type]
        for lc in livivo_clicks:
            for element, click in lc.items():
                if click:
                    if click_distr.get(element) is None:
                        click_distr[element] = 1
                    else:
                        click_distr[element] = click_distr[element] + 1
    return click_distr


def main():

    mkdir(RESULT_DIR)

    data = {}

    ranking_systems = systems.select().where(and_(systems.c.type != 'REC', systems.c.name != 'livivo_base')).execute().fetchall()
    ranking_systems = [r for r in ranking_systems if r.name not in NOT_PARTICIPATED]

    for system in ranking_systems:
        system_sessions = sessions.select(sessions.c.system_ranking == system.id).execute().fetchall()
        system_sessions_ids = [r.id for r in system_sessions]
        system_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(system_sessions_ids)).execute().fetchall()
        data[system.name] = livivo_click_distribution(system_feedbacks)
        data[''.join([system.name, '_base'])] = livivo_click_distribution(system_feedbacks, type='BASE')

    # livivo_base
    ranking_system_ids = [r.id for r in ranking_systems]
    system_sessions = sessions.select(sessions.c.system_ranking.in_(ranking_system_ids)).execute().fetchall()
    system_sessions_ids = [r.id for r in system_sessions]
    system_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(system_sessions_ids)).execute().fetchall()
    data['livivo_exp'] = livivo_click_distribution(system_feedbacks)
    data['livivo_base'] = livivo_click_distribution(system_feedbacks, type='BASE')

    pd.DataFrame.from_dict(data).transpose().fillna(0).astype(int).to_csv(os.path.join(RESULT_DIR, 'livivo_click_distribution.csv'))

    pass


if __name__ == '__main__':
    main()
