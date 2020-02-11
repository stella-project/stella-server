import os
import json
from flask import Flask, jsonify, g, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from datetime import datetime

from .models import Role, Result, Session, Feedback, System, User


def setup(db):

    db.drop_all()
    db.create_all()

    admin_role = Role(name='Admin')
    participant_role = Role(name='Participant')
    site_role = Role(name='Site')

    user_admin = User(username='STELLA-Admin', role=admin_role, password='pass')
    # print(user_admin.verify_password('pass'))
    user_part_a = User(username='Participant A', role=participant_role)
    user_part_b = User(username='Participant B', role=participant_role)
    user_site_a = User(username='Site A', role=site_role)
    user_site_b = User(username='Site B', role=site_role)

    # ranking = Result(system_id=)

    db.session.add_all([
        admin_role,
        participant_role,
        site_role,
        user_admin,
        user_part_a,
        user_part_b,
        user_site_a,
        user_site_b,
    ])

    db.session.commit()

    ranker_a = System(name='rank_exp_a', participant_id=user_part_a.id, type='RANK')
    ranker_b = System(name='rank_exp_b', participant_id=user_part_b.id, type='RANK')
    recommender_a = System(name='rec_exp_a', participant_id=user_part_a.id, type='REC')
    recommender_b = System(name='rec_exp_b', participant_id=user_part_b.id, type='REC')
    ranker_base_a = System(name='rank_base_a', participant_id=user_site_a.id, type='RANK')
    ranker_base_b = System(name='rank_base_b', participant_id=user_site_b.id, type='RANK')
    recommender_base_a = System(name='rec_base_a', participant_id=user_site_a.id, type='REC')
    recommender_base_b = System(name='rec_base_b', participant_id=user_site_b.id, type='REC')

    db.session.add_all([
        ranker_a,
        ranker_b,
        recommender_a,
        recommender_b,
        ranker_base_a,
        ranker_base_b,
        recommender_base_a,
        recommender_base_b
    ])

    db.session.commit()

    # session_site_a_rank_a_rec_a = Session(site_id=user_site_a.id,
    #                                       site_user='123.123.123.123',
    #                                       system_ranking=ranker_a.id,
    #                                       system_recommendation=recommender_a.id)
    #
    # session_site_a_rank_a_rec_b = Session(site_id=user_site_a.id,
    #                                       site_user='123.123.123.123',
    #                                       system_ranking=ranker_a.id,
    #                                       system_recommendation=recommender_b.id)
    #
    # session_site_b_rank_b_rec_b = Session(site_id=user_site_b.id,
    #                                       site_user='456.456.456.456',
    #                                       system_ranking=ranker_b.id,
    #                                       system_recommendation=recommender_b.id)
    #
    # session_site_b_rank_b_rec_a = Session(site_id=user_site_b.id,
    #                                       site_user='789.789.789.789',
    #                                       system_ranking=ranker_b.id,
    #                                       system_recommendation=recommender_a.id)
    #
    # db.session.add_all([
    #     session_site_a_rank_a_rec_a,
    #     session_site_a_rank_a_rec_b,
    #     session_site_b_rank_b_rec_b,
    #     session_site_b_rank_b_rec_a
    # ])
    #
    # db.session.commit()
    #
    # start = datetime.fromisoformat('2019-11-04T00:05:23')
    # end = datetime.fromisoformat('2019-11-04T00:10:38')
    # first_click = datetime.fromisoformat('2019-11-04T00:06:23')
    # second_click = datetime.fromisoformat('2019-11-04T00:08:15')
    #
    # interleave = {
    #     "doc1": None,
    #     "doc11": '2019-11-04T00:08:15',
    #     "doc2": None,
    #     "doc12": '2019-11-04T00:06:23',
    #     "doc3": None,
    #     "doc13": None,
    #     "doc4": None,
    #     "doc14": None,
    #     "doc5": None,
    #     "doc15": None,
    # }
    # feedback_site_a_rank_a = Feedback(start=start,
    #                                   end=end,
    #                                   session_id=session_site_a_rank_a_rec_a.id,
    #                                   site=user_site_a.id,
    #                                   interleave=True,
    #                                   clicks=interleave)
    #
    # db.session.add_all([
    #     feedback_site_a_rank_a
    # ])
    #
    # db.session.commit()
    #
    # query_date = datetime.fromisoformat('2019-11-04T00:05:23')
    #
    # items = {
    #     "0": "doc1",
    #     "1": "doc2",
    #     "2": "doc3",
    #     "3": "doc4",
    #     "4": "doc5",
    #     "5": "doc6",
    #     "6": "doc7",
    #     "7": "doc8",
    #     "8": "doc9",
    #     "9": "doc10"
    # }
    #
    # # items = 'asdf'
    #
    # ranking_base = Result(session_id=session_site_a_rank_a_rec_a.id,
    #                       system_id=ranker_base_a.id,
    #                       feedback_id=feedback_site_a_rank_a.id,
    #                       site_id=user_site_a.id,
    #                       type='RANK',
    #                       q='query_text',
    #                       q_date=query_date,
    #                       num_found=100,
    #                       page=1,
    #                       rpp=10,
    #                       items=json.dumps(items))
    #
    # items = {
    #     "0": "doc11",
    #     "1": "doc12",
    #     "2": "doc13",
    #     "3": "doc14",
    #     "4": "doc15",
    #     "5": "doc16",
    #     "6": "doc17",
    #     "7": "doc18",
    #     "8": "doc19",
    #     "9": "doc20"
    # }
    #
    # ranking_exp = Result(session_id=session_site_a_rank_a_rec_a.id,
    #                      system_id=ranker_a.id,
    #                      feedback_id=feedback_site_a_rank_a.id,
    #                      site_id=user_site_a.id,
    #                      type='RANK',
    #                      q='query_text',
    #                      q_date=query_date,
    #                      num_found=100,
    #                      page=1,
    #                      rpp=10,
    #                      items=json.dumps(items))
    #
    # db.session.add_all([
    #     ranking_base,
    #     ranking_exp
    # ])
    #
    # db.session.commit()
    #
    # db.create_all()