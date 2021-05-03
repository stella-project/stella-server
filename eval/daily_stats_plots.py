from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

DAILY_STATS_CSV = 'results/daily_stats.csv'

df = pd.read_csv(DAILY_STATS_CSV, index_col=0)

system_names = [system.name for system in systems.select(not_(systems.c.name.in_(NOT_PARTICIPATED))).execute().fetchall()]

for system_name in system_names:

    df_sys = df.loc[['_'.join([system_name, 'sessions']), '_'.join([system_name, 'impressions'])]]
    df_sys.index = ['Sessions', 'Impressions']
    ax = df_sys.transpose().plot.bar(figsize=(16, 4))
    ax.legend(loc='upper right')
    plt.title(' '.join(['Sessions vs. Impressions -', system_name]))
    plt.savefig(os.path.join(RESULT_DIR, '_'.join([system_name, 'sessions_vs_impressions.pdf'])),
                             format='pdf', bbox_inches='tight')
    plt.savefig(os.path.join(RESULT_DIR, '_'.join([system_name, 'sessions_vs_impressions.svg'])),
                             format='svg', bbox_inches='tight')
    plt.show()

    df_sys = df.loc[['_'.join([system_name, 'clicks']), '_'.join([system_name, 'clicks_base'])]]
    df_sys.index = ['Clicks (EXP)', 'Clicks (BASE)']
    ax = df_sys.transpose().plot.bar(figsize=(16, 4))
    ax.legend(loc='upper right')
    plt.title(' '.join(['Number of clicks -', system_name]))
    plt.savefig(os.path.join(RESULT_DIR, '_'.join([system_name, 'clicks.pdf'])),
                             format='pdf', bbox_inches='tight')
    plt.savefig(os.path.join(RESULT_DIR, '_'.join([system_name, 'clicks.svg'])),
                             format='svg', bbox_inches='tight')
    plt.show()
