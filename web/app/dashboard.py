from .models import System, Session, Feedback, User, Result
from .main.forms import Dropdown


class Dashboard:

    def __init__(self, user_id, system_id=None, site_id=None):

        user_role_id = User.query.filter_by(id=user_id).first().role_id

        self.system_id = system_id
        self.site_id = site_id

        if user_role_id == 3:  # user is site
            self.site_id = user_id

        if user_role_id == 1:  # user is admin
            self.systems = System.query.filter().distinct().all()
        if user_role_id == 2:  # user is participant
            self.systems = System.query.filter_by(participant_id=user_id).all()
        if user_role_id == 3:  # user is site
            system_ids = Session.query.filter_by(site_id=user_id).with_entities(Session.system_recommendation).distinct().all() + Session.query.filter_by(site_id=user_id).with_entities(Session.system_ranking).distinct().all()
            self.systems = System.query.filter(System.id.in_([s[0] for s in system_ids])).all()

        site_ids = Session.query.filter(Session.system_ranking.in_([r.id for r in self.systems])).with_entities(Session.site_id).distinct().all() + Session.query.filter(Session.system_recommendation.in_([r.id for r in self.systems])).with_entities(Session.site_id).distinct().all()

        if user_role_id == 1:  # user is admin
            self.sites = User.query.filter_by(role_id=3).distinct().all()
        if user_role_id == 2:  # user is participant
            self.sites = User.query.filter(User.id.in_([s[0] for s in site_ids])).all()
        if user_role_id == 3:  # user is site
            self.sites = [User.query.filter_by(id=user_id).first()]

        self.form = Dropdown()
        self.sessions = []
        self.clicks_base = {}
        self.clicks_exp = {}
        self.clicks_base = {}
        self.clicks_exp = {}
        self.feedbacks = {}
        self.impressions = {}
        self.win = 0
        self.loss = 0
        self.tie = 0
        self.outcome = 0
        self.CTR = 0

        try:
            if self.system_id == None: # get first ranker of participant
                self.ranker = self.systems[0]
            else:
                self.ranker = System.query.filter_by(id=self.system_id).first()

            if self.site_id == None: # get first site at which ranker is deployed
                self.site = Session.query.with_entities(Session.site_id).distinct().filter_by(system_ranking=self.ranker.id).first()
            else:
                self.site = [User.query.filter_by(id=self.site_id).first().id]

            if self.site is not None:
                if self.ranker.type == 'RANK':
                    results = Result.query.filter_by(system_id=self.ranker.id, site_id=self.site_id, type='RANK').all()
                    session_ids = []
                    for r in results:
                        if r.session_id not in session_ids:
                            session_ids.append(r.session_id)
                    self.sessions = [Session.query.filter_by(id=sid, system_ranking=self.ranker.id, site_id=self.site[0]).one() for sid in session_ids]
                if self.ranker.type == 'REC':
                    results = Result.query.filter_by(system_id=self.ranker.id, site_id=self.site_id, type='REC').all()
                    session_ids = []
                    for r in results:
                        if r.session_id not in session_ids:
                            session_ids.append(r.session_id)
                    self.sessions = [Session.query.filter_by(id=sid, system_recommendation=self.ranker.id, site_id=self.site[0]).one() for sid in session_ids]

            sids = [s.id for s in self.sessions]
            self.feedbacks = Feedback.query.filter(Feedback.session_id.in_(sids)).all()

            for s in self.sessions:
                date = s.start.strftime('%Y-%m-%d')
                if self.impressions.get(date) is None:
                    self.impressions.update({date: 1})
                else:
                    self.impressions[date] = self.impressions[date] + 1

            for f in self.feedbacks:
                clicks = f.clicks
                cnt_base = 0
                cnt_exp = 0
                for c in clicks.values():
                    if c.get('clicked') and c.get('type') == 'EXP':
                        date = c.get('date')[:10]
                        if self.clicks_exp.get(date) is None:
                            self.clicks_exp.update({date: 1})
                        else:
                            self.clicks_exp[date] = self.clicks_exp[date] + 1
                        cnt_exp += 1
                    if c.get('clicked') and c.get('type') == 'BASE':
                        date = c.get('date')[:10]
                        if self.clicks_base.get(date) is None:
                            self.clicks_base.update({date: 1})
                        else:
                            self.clicks_base[date] = self.clicks_base[date] + 1
                        cnt_base += 1
                if cnt_exp > cnt_base:
                    self.win += 1
                if cnt_exp < cnt_base:
                    self.loss += 1
                if cnt_exp == cnt_base:
                    self.tie += 1

            if len(self.impressions) > 0:
                self.CTR = round(len(self.clicks_exp) / len(self.impressions), 4)

            if self.win > 0 or self.loss > 0:
                self.outcome = "{0:.4f}".format(self.win / (self.win + self.loss))
        except:
            pass

    def dropdown(self):

        self.form.system.choices = [(r.id, r.name) for r in self.systems]
        if len(self.form.system.choices) != 0:
            self.form.system.default = self.form.system.choices[0]
        self.form.site.choices = [(s.id, s.username) for s in self.sites]
        if len(self.form.site.choices) != 0:
            self.form.site.default = self.form.site.choices[0]
        return self.form

    def get_impressions(self):

        return dict(
            data=[
                dict(
                    x=list(self.impressions.keys()),
                    y=list(self.impressions.values()),
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

    def get_clicks(self):

        return dict(
            data=[
                dict(
                    x=list(self.clicks_base.keys()),
                    y=list(self.clicks_base.values()),
                    name='Site',

                    # type='scatter'
                    type='bar'
                ),
                dict(
                    x=list(self.clicks_exp.keys()),
                    y=list(self.clicks_exp.values()),
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

    def get_pie_chart(self):

        return dict(
            data=[
                dict(
                    values=[self.win, self.loss, self.tie],
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

    def get_table(self):

        return dict(
            data=[
                dict(type='table',
                     header=dict(values=['Metric', 'Value'],
                                 align='left', fill={"color": "#201C2D"},
                                 line={"width": "1", "color": 'black'},
                                 font={"family": "Arial",
                                       "size": "12",
                                       "color": "white"}),
                     cells=dict(values=[['Win', 'Loss', 'Tie', 'Outcome', 'CTR'],
                                        [self.win, self.loss, self.tie, self.outcome, self.CTR]],
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
