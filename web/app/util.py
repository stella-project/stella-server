from .models import Role, System, User


def setup_db(db):
    db.drop_all()
    db.create_all()

    admin_role = Role(name='Admin')
    participant_role = Role(name='Participant')
    site_role = Role(name='Site')

    user_admin = User(username='STELLA-Admin', email='admin@stella.org', role=admin_role, password='pass')
    user_part_a = User(username='Participant A', email='participant_a@stella.org', role=participant_role, password='pass')
    user_part_b = User(username='Participant B', email='participant_b@stella.org', role=participant_role, password='pass')
    user_site_a = User(username='Site A', email='site_a@stella.org', role=site_role, password='pass')
    user_site_b = User(username='Site B', email='site_b@stella.org', role=site_role, password='pass')

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
