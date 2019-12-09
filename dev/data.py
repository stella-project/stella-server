import json


class Ranking:
    def __init__(self, qid, time, ranking):
        self.qid = qid
        self.time = time
        self.ranking = ranking

    def wins(self):
        # use ranking list here to count number of wins
        site = 0
        participant = 0

        for i in self.ranking:
            if i.get('clicked') is True and i.get('team') == 'participant':
                participant += 1

            if i.get('clicked') is True and i.get('team') == 'site':
                site += 1

        result = site, participant
        return result



def loadData():

    with open('../trecos/2016/citeseerx/queries.json', 'r') as f:
        data = (line.strip() for line in f)  # Aufteilen in Liste mit Dictionarys
        data_json = "[{0}]".format(','.join(data))

    queries = json.loads(data_json)

    with open('../trecos/2016/citeseerx/round1_test.json', 'r') as f:
        data = (line.strip() for line in f)
        data_json = "[{0}]".format(','.join(data))

    round1_test = json.loads(data_json)
    RankDict = {}
    for i in round1_test:
        RankDict[i.get('sid')] = Ranking(i.get('qid'), i.get('time'), i.get('ranking'))
    return RankDict
