from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')


def get_wlt(feedbacks):

    win = 0
    loss = 0
    tie = 0

    for feedback in feedbacks:
        exp_click = 0
        base_click = 0

        for doc in feedback.clicks.values():
            if doc.get('clicked') and doc.get('type') == 'EXP':
                exp_click += 1
            if doc.get('clicked') and doc.get('type') == 'BASE':
                base_click += 1

        if exp_click == base_click and exp_click > 0:
            tie += 1
        if exp_click > base_click:
            win += 1
        if base_click > exp_click:
            loss += 1

    return {'win': win,
            'loss': loss,
            'tie': tie}


def main():
    mkdir(RESULT_DIR)
    all_systems = systems.select().where(not_(systems.c.name.in_(NOT_PARTICIPATED))).execute().fetchall()
    for system in all_systems:
        wlt = {}
        if system.type == 'RANK':
            system_sessions = sessions.select(sessions.c.system_ranking == system.id).order_by(sessions.c.start).execute().fetchall()
        if system.type == 'REC':
            system_sessions = sessions.select(sessions.c.system_recommendation == system.id).order_by(sessions.c.start).execute().fetchall()
        for session in system_sessions:
            system_feedbacks = feedbacks.select(feedbacks.c.session_id == session.id).execute().fetchall()
            wlt[session.start] = get_wlt(system_feedbacks)
        df = pd.DataFrame.from_dict(wlt)
        if not df.empty:
            if OUTCOME:
                df = df.transpose().cumsum()
                df['outcome'] = df['win'] / (df['win'] + df['loss'])
                ax = df.plot(secondary_y=['outcome'], mark_right=False)
                # ax.legend(loc='center left', bbox_to_anchor=(1.2, 0.5))
                ax.set_ylabel('Total number of Wins, Losses, Ties')
                ax.right_ax.set_ylabel('Outcome')
                # df[['win', 'loss', 'tie']].plot()
                # ax = df['outcome'].plot(secondary_y=True)
                plt.title(' - '.join([system.name, 'Cumulative Wins, Losses, and Ties + Outcome']))

                plt.savefig(os.path.join(RESULT_DIR, '_'.join([system.name, 'wlt_vs_sessions_outcome.pdf'])),
                            format='pdf', bbox_inches='tight')
                plt.savefig(os.path.join(RESULT_DIR, '_'.join([system.name, 'wlt_vs_sessions_outcome.svg'])),
                            format='svg', bbox_inches='tight')
                plt.show()

            else:
                df.transpose().cumsum().plot.line()
                plt.title(' - '.join([system.name, 'Cumulative Wins, Losses, and Ties']))
                plt.savefig(os.path.join(RESULT_DIR, '_'.join([system.name, 'wlt_vs_sessions.pdf'])),
                            format='pdf', bbox_inches='tight')
                plt.savefig(os.path.join(RESULT_DIR, '_'.join([system.name, 'wlt_vs_sessions.svg'])),
                            format='svg', bbox_inches='tight')
                plt.show()




if __name__ == '__main__':
    main()
