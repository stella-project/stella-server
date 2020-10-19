import re
import os

from github import Github
from datetime import datetime


class Bot:

    def validate(self, TRECstr):
        print('validation started')
        errorLog = str()
        if TRECstr:
            lines = TRECstr.split('\n')[:-1]
            topics = {}
            for line in lines:
                if '\t' in line:
                    fields = line.split('\t')
                elif ' ' in line:
                    fields = line.split(' ')
                else:
                    errorLog += 'Error Line {} - Could not detect delimeter.\n'.format(str(lines.index(line) + 1))
                    continue

                if lines.index(line) == 0:
                    runTag = fields[5]

                if len(fields) != 6:
                    errorLog += 'Error Line {} - Missing fields.\n'.format(str(lines.index(line) + 1))
                    continue

                if not re.search("^[A-Za-z0-9_.-]{1,24}$", fields[5]):
                    errorLog += 'Error Line {} - Run tag {} is malformed.\n'.format(str(lines.index(line) + 1),
                                                                                    str(fields[5]))
                    continue
                else:
                    if not fields[5] == runTag:
                        errorLog += 'Error Line {} - Run tag is inconsistent ({} and {}).\n'.format(
                            str(lines.index(line) + 1),
                            str(fields[5]), str(runTag))
                        continue
                if not fields[0].isdigit():
                    errorLog += 'Error Line {} - Unknown topic {}.\n'.format(str(lines.index(line) + 1), str(fields[0]))
                    continue
                else:
                    if fields[0] not in topics:
                        topics[fields[0]] = 1
                    else:
                        topics[fields[0]] += 1
                    # todo: Topic anzahl abgleichen

                if 'Q0'.casefold() not in fields[1].casefold():
                    errorLog += 'Error Line {} - "Field 2 is {} not "Q0".\n'.format(str(lines.index(line) + 1),
                                                                                    str(fields[1]))
                    continue

                if not fields[3].isdigit():
                    errorLog += 'Error Line {} - "Column 4 (rank) {} must be an integer".\n'.format(
                        str(lines.index(line) + 1), str(fields[3]))
                    continue

                if not re.search("^[A-Za-z0-9-]{1,24}$", fields[2]):
                    errorLog += 'Error Line {} - "Invalid docid {}".\n'.format(str(lines.index(line) + 1),
                                                                               str(fields[2]))
                    continue

            print(errorLog)
        else:
            print('TREC file is empty!')
            return False

        if len(errorLog) == 0:
            print('validation successful')
            return True


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
