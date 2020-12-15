from .models import Role, System, User
import ruamel.yaml
import re
import tarfile
import os
import datetime


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def makeComposeFile():
    systems = System.query.filter_by().all()
    compose = {'version': '3',
               'networks': {'stella-shared': {'external': {'name': 'stella-server_default'}}},
            'services': {
                'app': {
                    'build': './app', 'volumes': ['/var/run/docker.sock/:/var/run/docker.sock', './app/log:/app/log'],
                    'ports': ["8080:8000"],
                    'depends_on': [system.name for system in systems],
                    'networks': ['stella-shared']
                    }
                }
            }
    for system in systems:
        compose['services'][str(system.name)] = {
            'build' : system.url,
            'container_name' : system.name,
            'volumes' : ['./data/:/data/'],
            'networks' : ['stella-shared']
        }
    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=4)

    with open('docker-compose.yml', 'w') as file:
        yaml.dump(compose, file)

    return True


def setup_db(db):
    '''
    Use this function to setup a database with set of pre-registered users.

    @param db: SQLAlchemy() instance.
    @return: -
    '''
    db.drop_all()
    db.create_all()

    admin_role = Role(name='Admin')
    participant_role = Role(name='Participant')
    site_role = Role(name='Site')

    user_admin = User(username='stella-admin',
                      email='admin@stella.org',
                      role=admin_role,
                      password='pass')

    user_part_a = User(username='participant_a',
                       email='participant_a@stella.org',
                       role=participant_role,
                       password='pass')

    user_part_b = User(username='participant_b',
                       email='participant_b@stella.org',
                       role=participant_role,
                       password='pass')

    user_site_a = User(username='GESIS',
                       email='gesis@stella.org',
                       role=site_role,
                       password='pass')

    user_site_b = User(username='LIVIVO',
                       email='livivo@stella.org',
                       role=site_role,
                       password='pass')

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

    # ranker_a = System(status='running', name='rank_elastic', participant_id=user_part_a.id, type='RANK', submitted='DOCKER', url='https://github.com/stella-project/rank_elastic.git')
    # ranker_b = System(status='submitted', name='experimental_ranker_b', participant_id=user_part_b.id, type='RANK', submitted='DOCKER', url='https://github.com/stella-project/rank_elastic.git')
    # recommender_a = System(status='error', name='recom_tfidf', participant_id=user_part_a.id, type='REC', submitted='DOCKER', url='https://github.com/stella-project/recom_tfidf.git')
    # recommender_b = System(status='running', name='experimental_recommender_b', participant_id=user_part_b.id, type='REC', submitted='DOCKER', url='https://github.com/stella-project/recom_tfidf.git')
    # ranker_base_a = System(status='running', name='rank_elastic_base', participant_id=user_site_a.id, type='RANK', submitted='DOCKER', url='https://github.com/stella-project/rank_elastic_base.git')
    # ranker_base_b = System(status='running', name='baseline_ranker_b', participant_id=user_site_b.id, type='RANK', submitted='DOCKER', url='https://github.com/stella-project/rank_elastic_base.git')
    # recommender_base_a = System(status='running', name='recom_tfidf_base', participant_id=user_site_a.id, type='REC', submitted='DOCKER', url='https://github.com/stella-project/recom_tfidf_base.git')
    # recommender_base_b = System(status='running', name='baseline_recommender_b', participant_id=user_site_b.id, type='REC', submitted='DOCKER', url='https://github.com/stella-project/recom_tfidf_base.git')

    # db.session.add_all([
    #     ranker_a,
    #     ranker_b,
    #     recommender_a,
    #     recommender_b,
    #     ranker_base_a,
    #     ranker_base_b,
    #     recommender_base_a,
    #     recommender_base_b
    # ])

    livivo_precom = System(status='running',
                           name='livivo_rank_precom',
                           participant_id=user_part_b.id,
                           type='RANK',
                           submitted='TREC',
                           url='https://github.com/stella-project/livivo_rank_precom',
                           site=user_site_b.id,
                           submission_date=datetime.date(2019, 6,10))

    livivo_base = System(status='running',
                         name='livivo_base',
                         participant_id=user_site_b.id,
                         type='RANK',
                         submitted='DOCKER',
                         url='https://github.com/stella-project/livivo_rank_base',
                         site=user_site_b.id,
                         submission_date=datetime.date(2019, 6,10))

    rank_pyterrier = System(status='running',
                            name='livivo_rank_pyterrier',
                            participant_id=user_part_b.id,
                            type='RANK',
                            submitted='DOCKER',
                            url='https://github.com/stella-project/livivo_rank_pyterrier',
                            site=user_site_b.id,
                            submission_date=datetime.date(2019, 6,10))

    rank_pyserini = System(status='running',
                            name='livivo_rank_pyserini',
                            participant_id=user_part_b.id,
                            type='RANK',
                            submitted='DOCKER',
                            url='https://github.com/stella-project/livivo_rank_pyserini',
                            site=user_site_b.id,
                            submission_date=datetime.date(2019, 6,10))

    rec_pyterrier = System(status='running',
                           name='gesis_rec_pyterrier',
                           participant_id=user_part_a.id,
                           type='REC',
                           submitted='DOCKER',
                           url='https://github.com/stella-project/gesis_rec_pyterrier',
                           site=user_site_a.id,
                           submission_date=datetime.date(2019, 6,10))

    rec_pyserini = System(status='running',
                          name='gesis_rec_pyserini',
                          participant_id=user_part_a.id,
                          type='REC',
                          submitted='DOCKER',
                          url='https://github.com/stella-project/gesis_rec_pyserini',
                          site=user_site_a.id,
                          submission_date=datetime.date(2019, 6,10))

    recommender_base_a = System(status='running',
                                name='gesis_rec_precom',
                                participant_id=user_site_a.id,
                                type='REC',
                                submitted='TREC',
                                url='https://github.com/stella-project/gesis_rec_precom',
                                site=user_site_a.id,
                                submission_date=datetime.date(2019, 6,10))

    # rec_whoosh = System(status='running', name='gesis_rec_whoosh', participant_id=user_part_b.id,
    #                     type='REC', submitted='DOCKER', url='https://github.com/stella-project/gesis_rec_whoosh',
    #                     site=user_site_a.id)
    # rec_shuffle = System(status='running', name='gesis_rec_micro', participant_id=user_site_a.id,
    #                      type='REC', submitted='DOCKER', url='https://github.com/stella-project/gesis_rec_micro',
    #                      site=user_site_a.id)

    db.session.add_all([
        livivo_base,
        livivo_precom,
        rank_pyserini,
        rank_pyterrier,
        recommender_base_a,
        rec_pyterrier,
        rec_pyserini,
    ])

    db.session.commit()
