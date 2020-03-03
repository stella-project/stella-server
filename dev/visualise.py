from dev import data
import matplotlib.pyplot as plt
import mpld3
import plotly.offline
import json

# Skript zum visualisieren der Daten in unterschiedlichen Diagrammen durch zwei Methoden:
# 1. matplotlib und mpld3 - erstellt einen html plot der als iframe angezeigt werden kann
# 2. plotly - erstellt Diagramm anweisungen im json Format das durch javascript eingebunden wird.


# Visualisierung des Sitetraffics in einem Barplot für jeden Tag
def traffic(library):
    test1 = data.loadData()
    traffic = {}
    time = []
    visits = []

# Data processing
    for i in test1:
        traffic[test1.get(i).time[:10]] = traffic.get(test1.get(i).time[:10], 0) + 1

    for key in traffic:
        time.append(key)
        visits.append(traffic.get(key))

# Data visualization plotly
    if library == 'plotly':

        htmlplot = dict(
            data=[
                dict(
                    x=time,
                    y=visits,
                    type='bar'
                ),
            ],
            layout=dict(
                title='Impressions',
                margin=dict(
                    l=15,
                    r=15,
                    t=50,
                    b=50
                )
            )
        )

# Data visualization matplotlib
    elif library == 'matplotlib':
        fig = plt.figure()  # Plot Variable
        y_pos = time
        plt.bar(y_pos, visits)  # Balken Plotten
        plt.xticks(y_pos, time, rotation=90)
        htmlplot = mpld3.fig_to_html(fig, template_type='simple')

    return htmlplot


# Visualisierung des Sitetraffics in einem Lineplot für jeden Tag
def lineplot(library):
    test1 = data.loadData()
    site = {}

# Data processing
    for i in test1:
        site[test1.get(i).time[:10]] = 0  # Nach Datum sortieren

    for i in test1:
        for doc in test1.get(i).ranking:
            if doc.get('clicked'):
                if doc.get('team') == 'site':
                    site[test1.get(i).time[:10]] += 1

    participant = {}
    for i in test1:
        participant[test1.get(i).time[:10]] = 0  # Nach Datum sortieren

    for i in test1:
        for doc in test1.get(i).ranking:
            if doc.get('clicked'):
                if doc.get('team') == 'participant':
                    participant[test1.get(i).time[:10]] += 1

    SiteZeit = []
    for key in site:
        SiteZeit.append(key)
    SiteBesuche = []
    for values in SiteZeit:
        SiteBesuche.append(site.get(values))

    PartZeit = []
    for key in participant:
        PartZeit.append(key)
    PartBesuche = []
    for values in PartZeit:
        PartBesuche.append(participant.get(values))

# Data visualization matplotlib
    if library == 'matplotlib':
        fig = plt.figure()
        plt.plot(SiteZeit, SiteBesuche, label='Site')
        plt.plot(PartZeit, PartBesuche, label='Participant')

        plt.xticks(SiteZeit, SiteZeit, rotation=0)

        plt.xlabel('Day')
        plt.ylabel('Clicks')
        plt.title('clicks per day and team')
        plt.legend()

        htmlplot = mpld3.fig_to_html(fig, template_type='simple')

# Data visualization matplotlib
    elif library == 'plotly':
        htmlplot = dict(
            data=[
                dict(
                    x=SiteZeit,
                    y=SiteBesuche,
                    name='Site',

                    # type='scatter'
                    type='bar'
                ),
                dict(
                    x=PartZeit,
                    y=PartBesuche,
                    name='Part',

                    # type='scatter'
                    type='bar'
                ),
            ],
            layout=dict(
                title='Clicks',
                margin=dict(
                    l=15,
                    r=15,
                    t=50,
                    b=50
                )
            )
        )

    return htmlplot


# Funktion zum erstellen eines Kreisdiagramms mit plotly aus den Werten Wins, losses, und Ties
def stats():
    wins = 0
    loss = 0
    tie = 0
    test1 = data.loadData()
    for i in test1:
        if test1.get(i).wins()[0] < test1.get(i).wins()[1]:
            wins += 1
        elif test1.get(i).wins()[0] > test1.get(i).wins()[1]:
            loss += 1
        elif test1.get(i).wins()[0] == test1.get(i).wins()[1]:
            tie += 1

    htmlplot = dict(
        data=[
            dict(
                values=[wins, loss, tie],
                labels=['wins', 'loss', 'tie'],
                hole=.3,
                type='pie'
            ),
        ],
        layout=dict(
            title='Wins, Losses and Ties',
            margin=dict(
                l=15,
                r=15,
                t=50,
                b=50
            )
        )
    )

    return htmlplot


# Funktion zum erstteln  einer plotly Tabelle mit Kennzahlen
def outcome():
    wins = 0
    loss = 0
    tie = 0
    clicks = 0
    views = 0

    test1 = data.loadData()
    impressions = len(test1)
    for i in test1:
        clicks += test1[i].clicks()
        if test1.get(i).wins()[0] < test1.get(i).wins()[1]:
            wins += 1
        elif test1.get(i).wins()[0] > test1.get(i).wins()[1]:
            loss += 1
        elif test1.get(i).wins()[0] == test1.get(i).wins()[1]:
            tie += 1

    CTR = round(clicks / impressions, 4)

    outcome = "{0:.4f}".format(wins / (wins + loss))

    htmlplot = dict(
        data=[
            dict(type='table',
                 header=dict(values=['Metric', 'Value'],
                             align='left', fill={"color": "#119DFF"},
                             line={"width": "1", "color": 'black'},
                             font={"family": "Arial",
                                   "size": "12",
                                   "color": "white"}),
                 cells=dict(values=[['Win', 'Loss', 'Tie', 'Outcome', 'CTR'], [wins, loss, tie, outcome, CTR]],
                            align='left',
                            line={"width": "1", "color": 'black'},
                            fill={"color": "#506784"},
                            font={"family": "Arial",
                                  "size": "12",
                                  "color": "white"})
                 )],
        layout=dict(
            # title='Wins, Losses and Ties',
            margin=dict(
                l=15,
                r=15,
                t=50,
                b=50
            ),

        )
    )

    return htmlplot


# Alle Plots in eine Json zusammenfügen
def makeJson():
    graphs = [traffic('plotly'), stats(), lineplot('plotly'), outcome()]

    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return ids, graphJSON
