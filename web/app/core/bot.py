import re
import os

from github import Github
from datetime import datetime



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
            lines = TRECstr.split('\n')[:-1]
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

                if not re.search("^[A-Za-z0-9-]{1,24}$", fields[2]):
                    error = 'Error line {} - "Invalid docid {}"\n'.format(str(lines.index(line) + 1),
                                                                          str(fields[2]))
                    errorLog.setdefault('docid', []).append(error)
                    continue

            if len(errorLog) == 0:
                return False
        else:
            return 'TREC file is empty!'
        return errorMessage(errorLog)


    def saveFile(self, TRECstr, filename):
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open(os.path.join('uploads', filename), 'w') as outfile:
            outfile.write(TRECstr)


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
    def create_new_precom_repo(token, repo_name, run_in):
        g = Github(token)
        user = g.get_user()
        orga = 'stella-project'
        stella_project = g.get_organization(orga)
        repo = stella_project.get_repo('stella-app')

        contents = repo.get_contents('rank_precom/')
        head_query_file = [file for file in repo.get_contents('rank_precom/data/topic/') if file.name == 'head_queries_rnd1.xml'][0]
        dockerfile = [file for file in contents if file.name == 'Dockerfile'][0]
        app_py = [file for file in contents if file.name == 'app.py'][0]
        requirements = [file for file in contents if file.name == 'requirements.txt'][0]

        repo_name = repo_name + '_precom'
        repo = stella_project.create_repo(repo_name, private=True)
        repo.create_file('Dockerfile', 'add Dockerfile', dockerfile.decoded_content.decode('utf-8'))
        repo.create_file('app.py', 'add app.py', app_py.decoded_content.decode('utf-8'))
        repo.create_file('requirements.txt', 'add requirements.txt', requirements.decoded_content.decode('utf-8'))
        repo.create_file('data/topic/head_queries_rnd1.xml', 'add head_queries_rnd1.xml',
                         head_query_file.decoded_content.decode('utf-8'))
        repo.create_file('data/run/run_rnd1.txt', 'add run file', run_in)
