from db import *


def filter_experimental_results(sys_res):
    items = list(sys_res.__getitem__('items').values())
    types = [i.get('type') for i in items]
    if 'EXP' in types and not 'BASE' in types:
        return True
    return False


def main():
    system_name = 'lemuren_elk'

    system = systems.select(systems.c.name==system_name).execute().first()
    system_sessions = sessions.select(sessions.c.system_ranking == system.id).execute().fetchall()
    session_ids = [s.id for s in system_sessions]

    system_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(session_ids)).execute().fetchall()
    system_feedbacks_ids = [f.id for f in system_feedbacks]

    system_results = results.select(results.c.feedback_id.in_(system_feedbacks_ids)).execute().fetchall()
    filtered_system_results = list(filter(filter_experimental_results, system_results))

    for sys_res in filtered_system_results:
        print(sys_res)


if __name__ == '__main__':
    main()
