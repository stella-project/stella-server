from dev import data
import matplotlib.pyplot as plt
import mpld3
import plotly.graph_objects as go



def traffic(library):
    test1 = data.loadData()
    traffic={}
    time=[]
    visits= []

    for i in test1:
        traffic[test1.get(i).time[:10]] = traffic.get(test1.get(i).time[:10], 0) + 1

    for key in traffic:
        time.append(key)
        visits.append(traffic.get(key))

    if library == 'plotly':
        fig = go.Figure(
            data=[go.Bar(y=visits)],
            layout_title_text="traffic",
        )
        htmlplot = fig.show(renderer="iframe")
        py.plot(plot_func, output_type='div')

    elif library == 'matplotlib' :
        fig = plt.figure()  # Plot Variable
        y_pos = time
        plt.bar(y_pos, visits)  # Balken Plotten
        plt.xticks(y_pos, time, rotation=90)
        #plt.show()
        htmlplot = mpld3.fig_to_html(fig, template_type='simple')


    htmlStart = """<html lang="de">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Titel der Seite | Name der Website</title>
  </head>

  <body>"""

    htmlEnd = """  </body>
</html>"""
    # return htmlStart + htmlplot + htmlEnd
    return htmlplot





# Ausgabe als Lineplot
def lineplot():
    test1 = data.loadData()
    site = {}
    for i in test1:
        site[test1.get(i).time[:10]] = 0  # Nach Datum sortieren

    for i in test1:
        for doc in test1.get(i).ranking:
            if doc.get('clicked'):
                if doc.get('team') == 'site':
                    site[test1.get(i).time[:10]] += 1

    participant = {}
    for i in test1:
        participant[i['time'][:10]] = 0  # Nach Datum sortieren

    for i in test1:
        for doc in i.get('ranking'):
            if doc.get('clicked'):
                if doc.get('team') == 'participant':
                    participant[i['time'][:10]] += 1

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

    fig = plt.figure()
    plt.plot(SiteZeit, SiteBesuche, label='Site')
    plt.plot(PartZeit, PartBesuche, label='Participant')

    plt.xticks(SiteZeit, SiteZeit, rotation=0)

    plt.xlabel('Day')
    plt.ylabel('Clicks')
    plt.title('clicks per day and team')
    plt.legend()

    plt.show()
    mpld3.show()

    htmlplot = mpld3.fig_to_html(fig)
    return htmlplot