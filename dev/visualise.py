from dev import data
import matplotlib.pyplot as plt
import mpld3
import plotly.graph_objects as go
import plotly.offline



def traffic(library):
    test1 = data.loadData()
    traffic={}
    time=[]
    visits= []

    #Data processing
    for i in test1:
        traffic[test1.get(i).time[:10]] = traffic.get(test1.get(i).time[:10], 0) + 1

    for key in traffic:
        time.append(key)
        visits.append(traffic.get(key))

    #Data visualization
    if library == 'plotly':
        fig = go.Figure(
            data=[go.Bar(y=visits)],
            #layout_title_text="traffic",
        )
        # htmlplot = fig.show(renderer="iframe")
        # htmlplot = fig.show(output_type='div')
        skript = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
        htmlplot = skript + plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    elif library == 'matplotlib':
        fig = plt.figure()  # Plot Variable
        y_pos = time
        plt.bar(y_pos, visits)  # Balken Plotten
        plt.xticks(y_pos, time, rotation=90)
        #plt.show()
        htmlplot = mpld3.fig_to_html(fig, template_type='simple')


    return htmlplot





# Ausgabe als Lineplot
def lineplot(library):
    test1 = data.loadData()
    site = {}

    #Data processing
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

    elif library == 'plotly':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=SiteZeit ,y=SiteBesuche,
            mode='lines',
            name='lines'))

        fig.add_trace(go.Scatter(x=PartZeit, y=PartBesuche,
                                 mode='lines',
                                 name='lines'))

        skript = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
        htmlplot = skript + plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')




    return htmlplot