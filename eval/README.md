### Setup

Setup a Postgres instance via Docker:

```
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
```

Restore database after you have retrieved a recent dump:

```
export PGPASSWORD=postgres && pg_restore -h localhost -d postgres <dump-file-name>.tar -c -U postgres
```

Install Python packages:

```
pip install -r requirements.txt
```

### Overview

| Script | Output | Description | Requirements |
| --- | --- | --- | --- |
| `daily_stats.py` | `results/daily_stats.csv` | Outputs a csv file with the total number of sessions, impressions, clicks, and clicks of the baseline for each system on a daily basis. | **Running database** |
| `livivo_click_distribution.py` | `results/livivo_click_distribution.pdf` | Outputs a bar histogram with click counts across SERP elements. |  **Running database** |
| `livivo_click_distribution_single_systems.py` | `results/livivo_click_distribution.csv` | Outputs a csv file with click counts across SERP elements for each system. | **Running database** |
| `overall_stats.py` | `results/overall_stats.csv` | Outputs a csv file with Wins, Losses, Ties, ... for each system. |  **Running database** |
| `daily_stats_plots.py` | Several plots | Outputs bar charts with `sessions vs. impressions` and `number of clicks - exp vs. base` | **Running database**, `results/overall_stats.csv` |
| `pie_charts.py` | Several plots | Outputs several plots with pie charts containing Wins, Losses, and Ties | `results/overall_stats.csv` |
