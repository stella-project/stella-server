import re
import os

from github import Github
from datetime import datetime

from ..util import make_tarfile

from ..models import System
import ruamel.yaml


class Bot:

    def validate(self, TRECstr):
        def errorMessage(errorLog):
            message = []
            errorcount = sum([len(errorLog[s]) for s in errorLog])
            message.append('Validation failed! There are {} errors in your file.'.format(str(errorcount)))
            for errorType in errorLog:
                if len(errorLog[errorType]) > 1:
                    message.append(
                        errorLog[errorType][0] + ' and {} more lines.'.format(str(len(errorLog[errorType]) - 1)))
                else:
                    message.append(errorLog[errorType][0])
            return message

        errorLog = {}
        if TRECstr:
            TRECstr_decoded = TRECstr.read().decode("utf-8")
            lines = TRECstr_decoded.split('\n')[:-1]
            topics = {}
            for line in lines:
                if '\t' in line:
                    fields = line.split('\t')
                elif ' ' in line:
                    fields = line.split(' ')
                else:
                    error = 'Error line {} - Could not detect delimeter\n'.format(str(lines.index(line) + 1))
                    errorLog.setdefault('wrong delimeter', []).append(error)
                    continue

                if lines.index(line) == 0:
                    runTag = fields[5]

                if len(fields) != 6:
                    error = 'Error line {} - Missing fields\n'.format(str(lines.index(line) + 1))
                    errorLog.setdefault('missing fields', []).append(error)
                    continue

                if not re.search("^[A-Za-z0-9_.-]{1,24}$", fields[5]):
                    error = 'Error line {} - Run tag {} is malformed\n'.format(str(lines.index(line) + 1),
                                                                               str(fields[5]))
                    continue
                else:
                    if not fields[5] == runTag:
                        error = 'Error line {} - Run tag is inconsistent ({} and {})\n'.format(
                            str(lines.index(line) + 1),
                            str(fields[5]), str(runTag))
                        errorLog.setdefault('inconsistent run tag', []).append(error)
                        continue
                if not fields[0].isdigit():
                    error = 'Error line {} - Unknown topic {}\n'.format(str(lines.index(line) + 1), str(fields[0]))
                    errorLog.setdefault('unknown topic', []).append(error)
                    continue
                else:
                    if fields[0] not in topics:
                        topics[fields[0]] = 1
                    else:
                        topics[fields[0]] += 1
                    # todo: Topic anzahl abgleichen

                if 'Q0'.casefold() not in fields[1].casefold():
                    error = 'Error line {} - "Field 2 is {} not "Q0"\n'.format(str(lines.index(line) + 1),
                                                                               str(fields[1]))
                    errorLog.setdefault('Q0', []).append(error)
                    continue

                if not fields[3].isdigit():
                    error = 'Error line {} - "Column 4 (rank) {} must be an integer"\n'.format(
                        str(lines.index(line) + 1), str(fields[3]))
                    errorLog.setdefault('rank', []).append(error)
                    continue

                # if not re.search("^[A-Za-z0-9-]{1,24}$", fields[2]):
                    # error = 'Error line {} - "Invalid docid {}"\n'.format(str(lines.index(line) + 1),
                                                                          # str(fields[2]))
                    # errorLog.setdefault('docid', []).append(error)
                    # continue

            if len(errorLog) == 0:
                return False
        else:
            return 'TREC file is empty!'
        return errorMessage(errorLog)

    def compressFile(self, subdir):

        input = os.path.join(subdir, 'run.txt')
        output = os.path.join(subdir, 'run.tar.gz')
        make_tarfile(output, input)
        return output

    def saveFile(self, file, filename):
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        subdir = os.path.join('uploads', filename)
        if not os.path.exists(subdir):
            os.makedirs(subdir)

        run_path = os.path.join(subdir, 'run.txt')

        file.save(run_path)

        return subdir



    def saveSplits(self, TRECstr, filename):
        files = {}
        lines = TRECstr.split('\n')[:-1]
        for line in lines:
            if '\t' in line:
                fields = line.split('\t')
            elif ' ' in line:
                fields = line.split(' ')
            else:
                print('Error Line {} - Could not detect delimeter.\n'.format(str(lines.index(line) + 1)))

            files.setdefault(fields[0], []).append(line)
        if not os.path.exists(os.path.join('uploads', str(filename.split('.')[0]))):
            os.makedirs(os.path.join('uploads', str(filename.split('.')[0])))
        for file in files:
            with open(os.path.join('uploads', str(filename.split('.')[0]),
                                   str(filename.split('.')[0]) + '_' + file + '.txt'), 'w') as outfile:
                for line in files[file]:
                    outfile.write(line + '\n')
        return files

    @staticmethod
    def push_to_github(token, repo_name):
        g = Github(token)
        repo = g.get_user().get_repo(repo_name)

        file = repo.get_contents('README.md')
        readme_content = file.decoded_content.decode('utf-8')

        commit_message = 'update at ' + str(datetime.now())
        updated_readme_content = readme_content + '  \n' + str(datetime.now())
        repo.update_file('README.md', commit_message, updated_readme_content, file.sha)

    @staticmethod
    def create_repo(token, repo_name, orga='stella-project'):
        g = Github(token)
        stella_project = g.get_organization(orga)
        stella_project.create_repo(repo_name, private=True)

    @staticmethod
    def create_precom_repo(token, repo_name, run_tar_in, type):
        g = Github(token)
        orga_name = 'stella-project'
        stella_project = g.get_organization(orga_name)
        template = stella_project.get_repo('stella-micro-template-precom')
        repo = stella_project.create_repo(repo_name + '_precom', private=True)

        for file in template.get_contents('.'):
            filename = file.name
            if filename not in ['test', 'precom']:
                commit_msg = 'add ' + filename
                repo.create_file(filename, commit_msg, file.decoded_content.decode('utf-8'))

        for test_file in template.get_contents('test'):
            filename = test_file.name
            commit_msg = 'add ' + filename
            repo.create_file('test/'+filename, commit_msg, test_file.decoded_content.decode('utf-8'))

        repo.create_file('precom/rank/.gitkeep', 'add rank dir', " ")
        repo.create_file('precom/rec/datasets/.gitkeep', 'add rec data dir', " ")
        repo.create_file('precom/rec/publications/.gitkeep', 'add rec pub dir', " ")

        if type == 'RANK':
            run_tar_path = 'precom/rank/run.tar.gz'
        if type == 'REC':
            run_tar_path = 'precom/rec/datasets/run.tar.gz'
        with open(run_tar_in, 'rb') as run_in:
            repo.create_file(run_tar_path, 'add run.tar.gz', run_in.read())

        return repo.html_url

    @staticmethod
    def update_stella_app(type='all', token=None):

        yml_path = 'uploads/docker-compose.yml'

        if type == 'all':
            systems = System.query.filter_by(status='running').all()
            repo_name = 'stella-app'
        if type == 'rec':
            systems = System.query.filter_by(type='REC', status='running').all()
            repo_name = 'stella-app'
        if type == 'rank':
            systems = System.query.filter_by(type='RANK', status='running').all()
            repo_name = 'stella-app'

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

        with open(yml_path, 'w') as file:
            yaml.dump(compose, file)

        with open(yml_path) as yml_in:
            updated_content = yml_in.read()
            print(updated_content)

        if token:
            g = Github(token)
            orga_name = 'stella-project'
            stella_project = g.get_organization(orga_name)
            stella_app = stella_project.get_repo(repo_name)

            file = stella_app.get_contents('docker-compose.yml')

            commit_message = 'automatic update'

            with open(yml_path) as yml_in:
                updated_content = yml_in.read()

            stella_app.update_file('docker-compose.yml', commit_message, updated_content, file.sha)
