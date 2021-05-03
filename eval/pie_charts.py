from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

STATS_CSV = 'results/overall_stats.csv'
df = pd.read_csv(STATS_CSV, index_col=0)

for row in df.iterrows():
    system_name = row[0]
    df.from_dict({row[0]:
                      {'Win': row[1]['Win'],
                       'Loss': row[1]['Loss'],
                       'Tie': row[1]['Tie']}
                  }).plot.pie(subplots=True)
    plt.legend(loc='upper right')
    centre_circle = plt.Circle((0, 0), 0.50, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.savefig(os.path.join(RESULT_DIR, '_'.join([system_name, 'pie.pdf'])),
                             format='pdf', bbox_inches='tight')
    plt.savefig(os.path.join(RESULT_DIR, '_'.join([system_name, 'pie.svg'])),
                             format='svg', bbox_inches='tight')

    plt.show()
