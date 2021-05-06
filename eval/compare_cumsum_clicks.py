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

df.loc[['livivo_base_clicks',
        'livivo_rank_pyserini_clicks',
        'lemuren_elastic_only_clicks',
        'lemuren_elastic_preprocessing_clicks']].transpose().cumsum().plot.line()

plt.show()
