"""

"""
import re


def parse_uploaded_file(filename):
    """
    Return parsed file in dict
    :param filename:
    :return:
    """
    list_of_lines = []

    # with codecs.open(filename, 'r', encoding='utf8') as file:
    for line in filename:
        line = line.decode('utf-8')
        line = line.replace('\ufeff', '')
        matched_time = re.match(r'\d\d:\d\d', line)
        if matched_time:
            edited_time = matched_time.group()
            old_time = line.split(',')[0]
            new_line = line.replace(old_time, edited_time).replace('\t', '').\
                replace('\n', '').replace('\r', '')
            list_of_lines.append(new_line)
        else:
            line = line.replace('\t', '').replace('\n', '').replace('\r', '')
            new_line = list_of_lines[-1] + line
            list_of_lines[-1] = new_line

    def parse_record(record):
        """
        Return one parsed record in dictionary
        :param record:
        :return: record_dict
        """

        record = record.split(',')

        # concatenate context item
        for item in record:
            if item.startswith('Context='):
                idx_start = record.index(item)

                new_context = ""
                for item in record[idx_start:]:
                    new_context += item

                del record[idx_start:]
                record.append(new_context)
                break

        # concatenate sql item
        for item in record:
            if item.startswith('Sql='):
                idx_start = record.index(item)
            if item.startswith('Rows='):
                idx_fin = record.index(item)

        new_sql = ""
        for item in record[idx_start:idx_fin]:
            new_sql += item

        del record[idx_start:idx_fin]
        record.insert(idx_start, new_sql)

        # concatenate new_plan_sql item
        for item in record:
            if item.startswith('planSQLText='):
                idx_start = record.index(item)
            if item.startswith('Context='):
                idx_fin = record.index(item)
            else:
                idx_fin = -1

        new_plan_sql = ""
        for item in record[idx_start:idx_fin]:
            new_plan_sql += item

        del record[idx_start:idx_fin]
        record.insert(idx_start, new_plan_sql)

        keys = ['time', 'DBMSSQL', 'number', 'processName',
                'process', 'OSThread', 'clientID',
                'applicationName', 'computerName', 'connectID',
                'SessionID', 'Usr', 'Trans', 'dbpid',
                'Sql', 'Rows', 'planSQLText', 'Context']

        record_dict = {}.fromkeys(keys)

        record_dict["time"] = record[0]
        record_dict['DBMSSQL'] = record[1]
        record_dict['number'] = record[2]

        for item in record:
            for key in keys[3:]:
                if key in item.split('=', maxsplit=1)[0]:
                    record_dict[key] = item.split('=', maxsplit=1)[1]
                    break

        return record_dict

    list_of_dicts = []
    for record in list_of_lines:
        list_of_dicts.append(parse_record(record))

    return list_of_dicts
