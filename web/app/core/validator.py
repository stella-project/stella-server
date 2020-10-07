import re


class Validator:

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
