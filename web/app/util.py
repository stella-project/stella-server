import ruamel.yaml
import re
import tarfile
import os
import glob
import time
import datetime
import random

from zipfile import ZipFile
from github import Github

from .models import Role, System, User


def mkdir(path):
    """Create directory if it does not exists.

    Args:
        path (str):  Directory path.

    """
    if not os.path.exists(path):
        os.makedirs(path)


def unpack(f_in, target_dir):
    """Unpack an archived run file and rename it to run.txt.

    Args:
        f_in (str): Filename or path to unpack.
        target_dir: Directory the file gets unpacked to.

    Returns:
        str: Path to unpacked file.

    """
    mkdir(target_dir)
    if f_in.endswith(('.xz', '.gz')):
        with tarfile.open(f_in) as tf_in:
            tf_in.extractall(target_dir)

    if f_in.endswith(('.zip')):
        with ZipFile(f_in) as zf_in:
            zf_in.extractall(target_dir)

    run_upload = glob.glob(os.path.join(target_dir, '*.txt'))[0]
    run_path = os.path.join(target_dir, 'run.txt')
    os.rename(run_upload, run_path)
    return run_path


def make_tarfile(output_filename, source_dir):
    """Create a tar archive from a given file in an given directory.

    Args:
        output_filename (str): Name and directory of the new archive.
        source_dir (str): Directory of the file to archive.

    """
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def makeComposeFile():
    """Creates an docker-compose.yaml file for the stella app.

    Returns:
        bool: True if successful

    """
    systems = System.query.filter_by().all()
    compose = {'version': '3',
               'networks': {'stella-shared': {'external': {'name': 'stella-server_default'}}},
               'services': {
                   'app': {
                       'build': './app',
                       'volumes': ['/var/run/docker.sock/:/var/run/docker.sock', './app/log:/app/log'],
                       'ports': ["8080:8000"],
                       'depends_on': [system.name for system in systems],
                       'networks': ['stella-shared']
                   }
               }
               }
    for system in systems:
        compose['services'][str(system.name)] = {
            'build': system.url,
            'container_name': system.name,
            'volumes': ['./data/:/data/'],
            'networks': ['stella-shared']
        }
    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=4)

    with open('docker-compose.yml', 'w') as file:
        yaml.dump(compose, file)

    return True


def setup_db(db):
    """Use this function to setup a database with set of pre-registered users.

    Args:
        db (object): SQLAlchemy() instance.

    """
    db.drop_all()
    db.create_all()

    admin_role = Role(name='Admin')
    participant_role = Role(name='Participant')
    site_role = Role(name='Site')

    user_admin = User(username='stella-admin',
                      email=os.environ.get('ADMIN_MAIL') or 'admin@stella-project.org',
                      role=admin_role,
                      password=os.environ.get('ADMIN_PASS') or 'pass')

    user_part_a = User(username='participant_a',
                       email=os.environ.get('PARTA_MAIL') or 'participant_a@stella-project.org',
                       role=participant_role,
                       password=os.environ.get('PARTA_PASS') or 'pass')

    user_part_b = User(username='participant_b',
                       email=os.environ.get('PARTB_MAIL') or 'participant_b@stella-project.org',
                       role=participant_role,
                       password=os.environ.get('PARTB_PASS') or 'pass')

    user_site_a = User(username='GESIS',
                       email=os.environ.get('GESIS_MAIL') or 'gesis@stella-project.org',
                       role=site_role,
                       password=os.environ.get('GESIS_PASS') or 'pass')

    user_site_b = User(username='LIVIVO',
                       email=os.environ.get('LIVIVO_MAIL') or 'livivo@stella-project.org',
                       role=site_role,
                       password=os.environ.get('LIVIVO_PASS') or 'pass')

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

    gesis_rank_pyserini = System(status='running',
                           name='gesis_rank_pyserini',
                           participant_id=user_part_a.id,
                           type='RANK',
                           submitted='DOCKER',
                           url='https://github.com/stella-project/gesis_rank_pyserini',
                           site=user_site_a.id,
                           submission_date=datetime.date(2019, 6, 10))

    gesis_rank_precom_base = System(status='running',
                           name='gesis_rank_precom_base',
                           participant_id=user_part_a.id,
                           type='RANK',
                           submitted='TREC',
                           url='https://github.com/stella-project/gesis_rank_precom_base',
                           site=user_site_a.id,
                           submission_date=datetime.date(2019, 6, 10))

    gesis_rank_precom = System(status='running',
                           name='gesis_rank_precom',
                           participant_id=user_part_b.id,
                           type='RANK',
                           submitted='TREC',
                           url='https://github.com/stella-project/gesis_rank_precom',
                           site=user_site_b.id,
                           submission_date=datetime.date(2019, 6, 10))

    gesis_rank_pyserini_base = System(status='running',
                           name='gesis_rank_pyserini_base',
                           participant_id=user_part_a.id,
                           type='RANK',
                           submitted='DOCKER',
                           url='https://github.com/stella-project/gesis_rank_pyserini_base',
                           site=user_site_a.id,
                           submission_date=datetime.date(2019, 6, 10))

    gesis_rec_pyserini = System(status='running',
                           name='gesis_rec_pyserini',
                           participant_id=user_part_a.id,
                           type='REC',
                           submitted='DOCKER',
                           url='https://github.com/stella-project/gesis_rec_pyserini',
                           site=user_site_a.id,
                           submission_date=datetime.date(2019, 6, 10))


    livivo_precom = System(status='running',
                           name='livivo_rank_precom',
                           participant_id=user_part_b.id,
                           type='RANK',
                           submitted='TREC',
                           url='https://github.com/stella-project/livivo_rank_precom',
                           site=user_site_b.id,
                           submission_date=datetime.date(2019, 6, 10))

    livivo_base = System(status='running',
                         name='livivo_base',
                         participant_id=user_site_b.id,
                         type='RANK',
                         submitted='DOCKER',
                         url='https://github.com/stella-project/livivo_rank_base',
                         site=user_site_b.id,
                         submission_date=datetime.date(2019, 6, 10))

    rank_pyterrier = System(status='running',
                            name='livivo_rank_pyterrier',
                            participant_id=user_part_b.id,
                            type='RANK',
                            submitted='DOCKER',
                            url='https://github.com/stella-project/livivo_rank_pyterrier',
                            site=user_site_b.id,
                            submission_date=datetime.date(2019, 6, 10))

    rank_pyserini = System(status='running',
                           name='livivo_rank_pyserini',
                           participant_id=user_part_b.id,
                           type='RANK',
                           submitted='DOCKER',
                           url='https://github.com/stella-project/livivo_rank_pyserini',
                           site=user_site_b.id,
                           submission_date=datetime.date(2019, 6, 10))

    rec_pyterrier = System(status='running',
                           name='gesis_rec_pyterrier',
                           participant_id=user_site_a.id,
                           type='REC',
                           submitted='DOCKER',
                           url='https://github.com/stella-project/gesis_rec_pyterrier',
                           site=user_site_a.id,
                           submission_date=datetime.date(2019, 6, 10))

    rec_pyserini = System(status='running',
                          name='gesis_rec_pyserini',
                          participant_id=user_part_a.id,
                          type='REC',
                          submitted='DOCKER',
                          url='https://github.com/stella-project/gesis_rec_pyserini',
                          site=user_site_a.id,
                          submission_date=datetime.date(2019, 6, 10))

    recommender_base_a = System(status='running',
                                name='gesis_rec_precom',
                                participant_id=user_part_a.id,
                                type='REC',
                                submitted='TREC',
                                url='https://github.com/stella-project/gesis_rec_precom',
                                site=user_site_a.id,
                                submission_date=datetime.date(2019, 6, 10))

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


def validate(ranking_str, k=None):
    """Validate a precomputed run file by the standardized TREC format.

    Args:
        ranking_str (str): run file as string.
        k (int): Number random sample lines to check

    Returns:
        bool/str: True: if no errors in run file. If errors exist, str: with error message.
    """
    def _construct_error_string(error_log):
        message = []
        error_count = sum([len(error_log[s]) for s in error_log])
        message.append('There are {} errors in your file:\n'.format(str(error_count)))
        for error_type in error_log:
            if len(error_log[error_type]) > 1:
                message.append(
                    error_log[error_type][0] + ' and {} more lines.\n'.format(str(len(error_log[error_type]) - 1)))
            else:
                message.append(error_log[error_type][0] + '\n')
        return message

    error_log = {}
    run_tag = {}
    topics = {}
    samples = []
    if ranking_str:
        ranking_str_decoded = ranking_str.read().decode("utf-8")
        lines = ranking_str_decoded.split('\n')[:-1]
        if k:
            for _ in range(0, k):
                s = lines[random.randint(0, len(lines) - 1)]
                samples.append(s)
        else:
            samples = lines

        for line in samples:
            if '\t' in line:
                fields = line.split('\t')
            elif ' ' in line:
                fields = line.split(' ')
            else:
                error_log.setdefault('wrong delimeter', []).append(
                    'Error line {} - Could not detect delimeter'.format(str(lines.index(line) + 1)))
                continue

            if len(fields) != 6:
                error_log.setdefault('missing fields', []).append(
                    'Error line {} - Missing fields'.format(str(lines.index(line) + 1)))
                continue

            run_tag.setdefault('run_tag', fields[5])
            if not re.search("^[A-Za-z0-9_.-]{1,24}$", fields[5]):
                error_log.setdefault('malformed run tag', []).append(
                    'Error line {} - Run tag {} is malformed'.format(str(lines.index(line) + 1),
                                                                     str(fields[5])))
                continue
            else:
                if not fields[5] == run_tag['run_tag']:
                    error_log.setdefault('inconsistent run tag', []).append(
                        'Error line {} - Run tag is inconsistent ({} and {})'.format(
                            str(lines.index(line) + 1),
                            str(fields[5]), str(run_tag['run_tag'])))
                    continue
            # todo: Topic anzahl abgleichen

            if 'Q0'.casefold() not in fields[1].casefold():
                error_log.setdefault('Q0', []).append('Error line {} - "Field 2 is {} not "Q0"'.format(
                    str(lines.index(line) + 1), str(fields[1])))
                continue

            if not fields[3].isdigit():
                error_log.setdefault('rank', []).append(
                    'Error line {} - "Column 4 (rank) {} must be an integer"'.format(
                        str(lines.index(line) + 1), str(fields[3])))
                continue

        if len(error_log) == 0:
            return False
    else:
        return 'Run file is empty!'
    return _construct_error_string(error_log)


def compress_file(subdir):
    """Compress the precomputed run file from the given subdir into a tar.gz archive.

    Args:
        subdir (str): Path to the directory containing the precomputed run file.

    Returns:
        str: Archive path.
    """
    input = os.path.join(subdir, 'run.txt')
    output = os.path.join(subdir, 'run.tar.gz')
    make_tarfile(output, input)
    return output


def save_file(file, systemname):
    """Create the directory for a submitted precomputed run file and save the run file to it.

    Args:
        file (object): Uploaded precomputed run file.
        systemname (str): User generated name for the submitted system.

    Returns:
        str: Path to the new created system subdirectory.
    """
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    subdir = os.path.join('uploads', systemname)
    if not os.path.exists(subdir):
        os.makedirs(subdir)

    run_path = os.path.join(subdir, 'run.txt')

    file.save(run_path)

    return subdir


def save_archive(archive, systemname):
    """Create the directory for a submitted precomputed run file archive, unpack the archive and save the run file to
    it.

    Args:
        archive (object):  Uploaded precomputed run file archive.
        systemname: User generated name for the submitted system.

    Returns:
        str: Path to the new created system subdirectory.
    """
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    subdir = os.path.join('uploads', systemname)
    if not os.path.exists(subdir):
        os.makedirs(subdir)

    save_path = os.path.join(subdir, archive.filename)

    archive.save(save_path)

    try:
        unpack(save_path, subdir)
    except Exception as e:
        print(str(e))

    return subdir


def create_repo(token, repo_name, orga='stella-project'):
    """Create a new GitHub repository inside an organization.

    Args:
        token (str): GitHub Authentication token.
        repo_name (str): Name of the new repository.
        orga (str): Name of the GitHub organization.

    Returns:

    """
    g = Github(token)
    stella_project = g.get_organization(orga)
    stella_project.create_repo(repo_name, private=True)


def create_precom_repo(token, repo_name, run_tar_in, type):
    """Create a new GitHub Repository from template for an uploaded precomputed run file inside our organization and
    push the precomputed run file to it.

    Args:
        token (str): GitHub Authentication token.
        repo_name (str): Name of the new repository.
        run_tar_in (str): Path to the precomputed run file.
        type (str): The task of the run file. RANK or REK.

    Returns:
        str: The URL of the new repository.
    """
    g = Github(token)
    orga_name = 'stella-project'
    stella_project = g.get_organization(orga_name)
    template = stella_project.get_repo('stella-micro-template-precom')
    repo = stella_project.create_repo(repo_name + '_precom', private=True)
    time.sleep(1)
    for file in template.get_contents('.'):
        filename = file.name
        if filename not in ['test', 'precom', 'resources', '.github']:
            commit_msg = 'add ' + filename
            repo.create_file(filename, commit_msg, file.decoded_content.decode('utf-8'))
            time.sleep(1)

    for test_file in template.get_contents('test'):
        filename = test_file.name
        commit_msg = 'add ' + filename
        repo.create_file('test/' + filename, commit_msg, test_file.decoded_content.decode('utf-8'))
        time.sleep(1)

    for workflow in template.get_contents('.github/workflows'):
        filename = workflow.name
        commit_msg = 'add ' + filename
        repo.create_file('.github/workflows/' + filename, commit_msg, workflow.decoded_content.decode('utf-8'))
        time.sleep(1)

        # head queries of livivo
    file_hq = template.get_contents('resources/livivo')[0]
    filename = file_hq.name
    commit_msg = 'add ' + filename
    repo.create_file('resources/livivo/' + filename, commit_msg, file_hq.decoded_content.decode('utf-8'))
    time.sleep(1)

    if type == 'RANK':
        run_tar_path = 'precom/rank/run.tar.gz'
    if type == 'REC':
        run_tar_path = 'precom/rec/datasets/run.tar.gz'
    with open(run_tar_in, 'rb') as run_in:
        repo.create_file(run_tar_path, 'add run.tar.gz', run_in.read())

    return repo.html_url


def create_stella_app_yaml(type='all', token=None):
    """Create a new docker-compose.yaml file for the STELLA app and push it to the STELLA app repository.
    All systems specified by type get included.

    Args:
        type (str): Type of the task. all, rec or rank.
        token (str): GitHub Authentication token.
    """

    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    if type == 'all':
        yml_path = 'uploads/stella-app.yml'
        systems = System.query.filter_by(status='running').all()
        repo_name = 'stella-app'
    if type == 'rec':
        yml_path = 'uploads/gesis.yml'
        systems = System.query.filter_by(type='REC', status='running').all()
        repo_name = 'stella-app'
    if type == 'rank':
        yml_path = 'uploads/livivo.yml'
        systems = System.query.filter_by(type='RANK', status='running').all()
        repo_name = 'stella-app'

    compose = {'version': '3',
               'services': {
                   'app': {
                       'build': './app',
                       'volumes': ['/var/run/docker.sock/:/var/run/docker.sock', './app/log:/app/log'],
                       'ports': ["8080:8000"],
                       'links': ['db:db'],
                       'depends_on': ['db'] + [system.name for system in systems]
                   },
                   'db': {
                       'image': 'postgres',
                       'ports': ['5432:5432'],
                       'environment': ['POSTGRES_USER=postgres', 'POSTGRES_PASSWORD=postgres', 'POSTGRES_DB=postgres']
                   }
               }
               }

    if type == 'all':
        ranksys = System.query.filter_by(type='RANK', status='running', submitted='DOCKER').all()
        ranksys_precom = System.query.filter_by(type='RANK', status='running', submitted='TREC').all()
        recsys = System.query.filter_by(type='REC', status='running', submitted='DOCKER').all()
        recsys_precom = System.query.filter_by(type='REC', status='running', submitted='TREC').all()

    if type == 'rank':
        ranksys = System.query.filter_by(type='RANK', status='running', submitted='DOCKER').all()
        ranksys_precom = System.query.filter_by(type='RANK', status='running', submitted='TREC').all()
        recsys = None
        recsys_precom = None

    if type == 'rec':
        ranksys = None
        ranksys_precom = None
        recsys = System.query.filter_by(type='REC', status='running', submitted='DOCKER').all()
        recsys_precom = System.query.filter_by(type='REC', status='running', submitted='TREC').all()

    compose['services']['app']['environment'] = []

    if ranksys:
        compose['services']['app']['environment'] = compose['services']['app']['environment'] + [
            'RANKSYS_LIST=' + ' '.join([sys.name for sys in ranksys])]

    if ranksys_precom:
        compose['services']['app']['environment'] = compose['services']['app']['environment'] + [
            'RANKSYS_PRECOM_LIST=' + ' '.join([sys.name for sys in ranksys_precom])]

    if ranksys or ranksys_precom:
        compose['services']['app']['environment'] = compose['services']['app']['environment'] + [
            'RANKSYS_BASE=livivo_base']

    if recsys:
        compose['services']['app']['environment'] = compose['services']['app']['environment'] + [
            'RECSYS_LIST=' + ' '.join([sys.name for sys in recsys])]

    if recsys_precom:
        compose['services']['app']['environment'] = compose['services']['app']['environment'] + [
            'RECSYS_PRECOM_LIST=' + ' '.join([sys.name for sys in recsys_precom])]

    if recsys or recsys_precom:
        compose['services']['app']['environment'] = compose['services']['app']['environment'] + [
            'RECSYS_BASE=gesis_rec_pyserini']

    compose['services']['app']['environment'] = compose['services']['app']['environment'] + [
        'STELLA_SERVER_ADDRESS=https://lilas.stella-project.org',
        'STELLA_SERVER_USER=gesis@stella-project.org',
        'STELLA_SERVER_PASS=pass',
        'STELLA_SERVER_USERNAME=GESIS',
        'INTERLEAVE=True',
        'BULK_INDEX=True',
        'DELETE_SENT_SESSION=True',
        'INTERVAL_DB_CHECK=3',
        'SESSION_EXPIRATION=6']

    for system in systems:
        # Please note: if you do not provide a GitHub token,
        # the docker-compose file will not differentiate between main and master branches!
        # This will make the build process of the stella-app fail in some cases with newer repositories.
        if token:
            g = Github(token)
            repo_id = '/'.join(system.url.split('/')[-2:])
            repo = g.get_repo(repo_id)
            branches_names = [branch.name for branch in repo.get_branches()]
            if 'main' in branches_names:
                gh_url = ''.join([system.url, '.git#main'])
            else:
                gh_url = ''.join([system.url, '.git#master'])
        else:
            gh_url = ''.join([system.url, '.git'])

        compose['services'][str(system.name)] = {
            'build': gh_url,
            'container_name': system.name,
            'volumes': ['./data/:/data/', ''.join([os.path.join('./index/', system.name), ':/index/'])]
        }

    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=4)

    with open(yml_path, 'w') as file:
        yaml.dump(compose, file)

    if token:
        g = Github(token)
        orga_name = 'stella-project'
        stella_project = g.get_organization(orga_name)
        stella_app = stella_project.get_repo(repo_name)

        if type == 'all':
            filename = 'stella-app.yml'
        if type == 'rec':
            filename = 'gesis.yml'
        if type == 'rank':
            filename = 'livivo.yml'

        file = stella_app.get_contents(filename)

        commit_message = 'automatic update'

        with open(yml_path) as yml_in:
            updated_content = yml_in.read()

        stella_app.update_file(filename, commit_message, updated_content, file.sha)
