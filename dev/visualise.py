from dev import data
import matplotlib.pyplot as plt
import mpld3
import plotly.graph_objects as go



def traffic():
    test1 = data.loadData()
    traffic={}
    time=[]
    visits= []

    for i in test1:
        traffic[test1.get(i).time[:10]] = traffic.get(test1.get(i).time[:10], 0) + 1

    for key in traffic:
        time.append(key)
        visits.append(traffic.get(key))


    fig = go.Figure(
        data=[go.Bar(y=visits)],
        layout_title_text="traffic",
    )

    figHTML = fig.show(renderer="iframe")



    # fig.show()

    # fig = plt.figure()  # Plot Variable
    # y_pos = time
    # plt.bar(y_pos, visits)  # Balken Plotten
    # plt.xticks(y_pos, time, rotation=90)
    # #plt.show()
    # htmlplot = mpld3.fig_to_html(fig, template_type='simple')

    return figHTML.get('text/html')





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