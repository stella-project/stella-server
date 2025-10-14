from app.extensions import db
from .main.forms import Dropdown
from .models import Feedback, Result, Session, System, User, Role


class Dashboard:

    def __init__(self, user_id, system_id=None, site_id=None):

        user_role_id = db.session.get(User, user_id).role_id
         
        admin_role = db.session.query(Role).filter_by(name='Admin').first()
        participant_role = db.session.query(Role).filter_by(name='Participant').first()
        site_role = db.session.query(Role).filter_by(name='Site').first()


        self.system_id = system_id
        self.site_id = site_id

        if user_role_id == site_role.id:  # user is site
            self.site_id = user_id

        if user_role_id == admin_role.id:  # user is admin
            self.systems = db.session.query(System).filter().distinct().all()
        if user_role_id == participant_role.id:  # user is participant
            self.systems = (
                db.session.query(System).filter_by(participant_id=user_id).all()
            )
        if user_role_id == site_role.id:  # user is site
            self.systems = db.session.query(System).filter(System.site == user_id).all()

        site_ids = (
            db.session.query(Session)
            .filter(Session.system_ranking.in_([r.id for r in self.systems]))
            .with_entities(Session.site_id)
            .distinct()
            .all()
            + db.session.query(Session)
            .filter(Session.system_recommendation.in_([r.id for r in self.systems]))
            .with_entities(Session.site_id)
            .distinct()
            .all()
        )

        if user_role_id == admin_role.id:  # user is admin
            self.sites = db.session.query(User).filter_by(role_id=site_role.id).distinct().all()
        if user_role_id == participant_role.id:  # user is participant
            self.sites = (
                db.session.query(User)
                .filter(User.id.in_([s[0] for s in site_ids]))
                .all()
            )
        if user_role_id == site_role.id:  # user is site
            self.sites = [db.session.query(User).filter_by(id=user_id).first()]

        self.form = Dropdown()
        self.sessions = []
        self.clicks_base = {}
        self.clicks_exp = {}
        self.clicks_base = {}
        self.clicks_exp = {}
        self.feedbacks = {}
        self.impressions = {}
        self.impressions_results = {}
        self.win = 0
        self.loss = 0
        self.tie = 0
        self.outcome = 0
        self.num_clicks = 0
        self.CTR = 0

        try:
            if self.system_id == None:  # get first ranker of participant
                self.ranker = self.systems[0]
            else:
                self.ranker = (
                    db.session.query(System).filter_by(id=self.system_id).first()
                )

            if self.site_id == None:  # get first site at which ranker is deployed
                self.site = (
                    db.session.query(Session)
                    .with_entities(Session.site_id)
                    .distinct()
                    .filter_by(system_ranking=self.ranker.id)
                    .first()
                )
            else:
                self.site = [
                    db.session.query(User).filter_by(id=self.site_id).first().id
                ]

            if self.site is not None:
                if self.ranker.type == "RANK":
                    results = (
                        db.session.query(Result)
                        .filter_by(
                            system_id=self.ranker.id, site_id=self.site_id, type="RANK"
                        )
                        .all()
                    )
                    session_ids = []
                    for r in results:
                        if r.session_id not in session_ids:
                            session_ids.append(r.session_id)
                    self.sessions = [
                        db.session.query(Session).filter_by(id=sid).first()
                        for sid in session_ids
                    ]
                if self.ranker.type == "REC":
                    results = (
                        db.session.query(Result)
                        .filter_by(
                            system_id=self.ranker.id, site_id=self.site_id, type="REC"
                        )
                        .all()
                    )
                    session_ids = []
                    for r in results:
                        if r.session_id not in session_ids:
                            session_ids.append(r.session_id)
                    self.sessions = [
                        db.session.query(Session).filter_by(id=sid).first()
                        for sid in session_ids
                    ]
            sids = [s.id for s in self.sessions]
            self.feedbacks = (
                db.session.query(Feedback).filter(Feedback.session_id.in_(sids)).order_by(Feedback.session_id).all()
            )

            for s in self.sessions:
                date = s.start.strftime("%Y-%m-%d")
                if self.impressions.get(date) is None:
                    self.impressions.update({date: 1})
                else:
                    self.impressions[date] = self.impressions[date] + 1

            _rid_date = []
            for r in results:
                date = r.q_date.strftime("%Y-%m-%d")
                if self.impressions_results.get(date) is None:
                    self.impressions_results.update({date: 1})
                    _rid_date.append((r.session_id, r.q_date))
                elif (r.session_id, r.q_date) not in _rid_date:
                    self.impressions_results[date] = self.impressions_results[date] + 1
                    _rid_date.append((r.session_id, r.q_date))

            prev_session_id = None
            prev_clicks = None
            for i, f in enumerate(self.feedbacks):
                clicks = f.clicks
                if f.session_id == prev_session_id:
                    for c in clicks:
                        if clicks[c].get('clicked'):
                            continue
                        elif prev_clicks[c].get('clicked'):
                            clicks[c]['clicked'] = True
                            clicks[c]['date'] = prev_clicks[c].get('date')
                
                prev_clicks = clicks
                prev_session_id = f.session_id

                if i + 1 < len(self.feedbacks) and f.session_id == self.feedbacks[i + 1].session_id:
                    continue

                cnt_base = 0
                cnt_exp = 0
                for c in clicks.values():
                    if c.get("clicked") and c.get("type") == "EXP":
                        date = c.get("date")[:10]
                        if self.clicks_exp.get(date) is None:
                            self.clicks_exp.update({date: 1})
                        else:
                            self.clicks_exp[date] = self.clicks_exp[date] + 1
                        cnt_exp += 1
                    if c.get("clicked") and c.get("type") == "BASE":
                        date = c.get("date")[:10]
                        if self.clicks_base.get(date) is None:
                            self.clicks_base.update({date: 1})
                        else:
                            self.clicks_base[date] = self.clicks_base[date] + 1
                        cnt_base += 1

                if cnt_base == 0 and cnt_exp == 0:
                    continue

                if cnt_exp > cnt_base:
                    self.win += 1
                if cnt_exp < cnt_base:
                    self.loss += 1
                if cnt_exp == cnt_base:
                    self.tie += 1

            # if displayed results are from the baseline system, flip wins and losses
            exp_sys = [
                db.session.query(Session)
                .filter(Session.id == self.feedbacks[0].session_id)
                .first()
                .system_ranking,
                db.session.query(Session)
                .filter(Session.id == self.feedbacks[0].session_id)
                .first()
                .system_recommendation,
            ]
            if not (int(self.system_id) in exp_sys):
                tmp = self.win
                self.win = self.loss
                self.loss = tmp
                self.num_clicks = sum(self.clicks_base.values())
            else:
                self.num_clicks = sum(self.clicks_exp.values())

            if len(self.impressions) > 0:
                self.CTR = round(
                    self.num_clicks / sum(self.impressions_results.values()), 4
                )

            if self.win > 0 or self.loss > 0:
                self.outcome = "{0:.4f}".format(self.win / (self.win + self.loss))
        except:
            pass

    def dropdown(self):
        self.form.system.choices = [
            (
                r.id,
                r.name
                + "@"
                + db.session.query(User).filter_by(id=r.site).first().username,
            )
            for r in self.systems
        ]
        if len(self.form.system.choices) != 0:
            self.form.system.default = self.form.system.choices[0]
        return self.form

    def get_impressions(self):

        return dict(
            data=[
                dict(
                    x=list(self.impressions.keys()),
                    y=list(self.impressions.values()),
                    name="Sessions",
                    type="bar",
                    marker={"color": "rgb(26, 118, 255)"},
                ),
                dict(
                    x=list(self.impressions_results.keys()),
                    y=list(self.impressions_results.values()),
                    name="Impressions",
                    type="bar",
                    marker={"color": "rgb(55, 83, 109)"},
                ),
            ],
            layout=dict(
                title="Sessions & Impressions",
                margin=dict(l=40, r=15, t=50, b=50),
                legend=dict(
                    yanchor="top",
                    xanchor="right",
                    traceorder="reversed",
                    title_font_family="Times New Roman",
                    font=dict(size=12, color="black"),
                    bgcolor="LightSteelBlue",
                    borderwidth=1,
                ),
            ),
        )

    def get_clicks(self):

        return dict(
            data=[
                dict(
                    x=list(self.clicks_base.keys()),
                    y=list(self.clicks_base.values()),
                    name="BASE",
                    # type='scatter'
                    type="bar",
                    marker={"color": "rgb(26, 118, 255)"},
                ),
                dict(
                    x=list(self.clicks_exp.keys()),
                    y=list(self.clicks_exp.values()),
                    name="EXP",
                    # type='scatter'
                    type="bar",
                    marker={"color": "rgb(55, 83, 109)"},
                ),
            ],
            layout=dict(
                title="Clicks",
                margin=dict(l=40, r=15, t=50, b=50),
                legend=dict(
                    yanchor="top",
                    xanchor="right",
                    traceorder="reversed",
                    title_font_family="Times New Roman",
                    font=dict(size=12, color="black"),
                    bgcolor="LightSteelBlue",
                    borderwidth=1,
                ),
            ),
        )

    def get_pie_chart(self):

        return dict(
            data=[
                dict(
                    values=[self.win, self.loss, self.tie],
                    labels=["wins", "loss", "tie"],
                    hole=0.3,
                    type="pie",
                    marker={
                        "colors": [
                            "rgb(26, 118, 255)",
                            "rgb(55, 83, 109)",
                            "rgb(32, 28, 45)",
                        ]
                    },
                ),
            ],
            layout=dict(
                title="Wins, Losses and Ties", margin=dict(l=15, r=15, t=50, b=50)
            ),
        )

    def get_table(self):

        return dict(
            data=[
                dict(
                    type="table",
                    columnwidth=[25, 15, 100],
                    header=dict(
                        values=["Metric", "Value", "Explanation"],
                        align="center",
                        fill={"color": "rgb(32, 28, 45)"},
                        line={"width": "1", "color": "black"},
                        font={"family": "Arial", "size": "12", "color": "white"},
                    ),
                    cells=dict(
                        values=[
                            [
                                "Win",
                                "Loss",
                                "Tie",
                                "Outcome",
                                "Sessions",
                                "Impressions",
                                "Clicks",
                                "CTR",
                            ],
                            [
                                self.win,
                                self.loss,
                                self.tie,
                                self.outcome,
                                sum(self.impressions.values()),
                                sum(self.impressions_results.values()),
                                self.num_clicks,
                                self.CTR,
                            ],
                            [
                                "A system 'wins' if it has more clicks on results assigned to it by the interleaving than clicks on results by the baseline system.",
                                "Opposite of 'Win'. Number of times when the system has less clicks on results than the baseline system.",
                                "Equal number of clicks for your system and the baseline. Only results having at least two clicks are included.",
                                "#Wins / (#Wins + #Loss)",
                                "Total number of sessions for which your system was used.",
                                "Total number of results for which your system was used.",
                                "Total number of clicks your system received.",
                                "Click-through rate",
                            ],
                        ],
                        align="center",
                        line={"width": "1", "color": "black"},
                        fill={"color": "rgb(55, 83, 109)"},
                        font={"family": "Arial", "size": "12", "color": "white"},
                    ),
                )
            ],
            layout=dict(
                # title='Wins, Losses and Ties',
                margin=dict(l=15, r=15, t=50, b=50),
            ),
        )