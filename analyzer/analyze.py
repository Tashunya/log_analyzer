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

        keys = ['time', 'DBMSSQL', 'number', 'count', 'processName',
                'process', 'OSThread', 'clientID',
                'applicationName', 'computerName', 'connectID',
                'SessionID', 'Usr', 'Trans', 'dbpid',
                'Sql', 'Rows', 'planSQLText', 'Context']

        record_dict = {}.fromkeys(keys)

        record_dict["time"] = record[0]
        record_dict['DBMSSQL'] = record[1]
        record_dict['number'] = record[2]
        record_dict['count'] = 1

        for item in record:
            for key in keys[4:]:
                if key in item.split('=', maxsplit=1)[0]:
                    record_dict[key] = item.split('=', maxsplit=1)[1]
                    break

        return record_dict

    list_of_dicts = []
    for record in list_of_lines:
        list_of_dicts.append(parse_record(record))

    return list_of_dicts


def create_graph(df, choice_num):
    """
    Return graph_div
    :param df: pandas.DataFrame
    :param choice_num: str(num) where num in range (1, 17)
    :return: html div with graph
    """

    from plotly import offline
    import plotly.graph_objs as go

    CHOICES = {'1': 'time', '2': 'Usr', '3': "processName", '4': 'process',
               '5': 'OSThread', '6': 'clientID', '7': 'applicationName', '8': 'computerName',
               '9': 'connectID', '10': 'SessionID', '11': 'Trans', '12': 'dbpid',
               '13': 'Sql', '14': 'Rows', '15': 'planSQLText', '16': 'Context'}

    if choice_num not in CHOICES.keys():
        return "<h1> CHOICE is Wrong. Try again! </h1>"

    choice = CHOICES[choice_num]

    df1 = df[[choice, 'count']].groupby([choice]).count()

    graph_div = ""

    if choice_num == '1':
        df1 = df1.sort_index()  # сортировка по таймингу
        time_ax = list(df1.index)
        process_count = list(df1['count'])
        fig = go.Figure(layout={'title': 'Number of Processes vs Time'})
        bar = go.Bar(x=time_ax, y=process_count,
                     name='Number of Processes vs Time')
        fig.add_trace(bar)
        graph_div = offline.plot(fig, auto_open=False, output_type='div')

    else:
        df1 = df1.sort_values(by=['count'])  # сортировка по кол-ву процессов
        # объединить 5% значений в группу "Другие"
        total_sum = df1['count'].sum()
        percentile_5 = int(total_sum * 0.05)  # 5% от общего числа процессов
        df1['cumsum'] = df1['count'].cumsum()  # столбец с накоплением суммы процессов
        limit = df1.iloc[
            (df1['cumsum'] - percentile_5).abs().argsort()[:1]]  # строка, ближайшая к 5%
        limit_num = int(limit['cumsum'])  # кол-во процессов
        df1 = df1[df1['cumsum'] > limit_num]  # убрать лишние строки с низкими значениями
        df1.loc["Другие"] = {'count': limit_num, 'cumsum': limit_num}  # добавить строку "Другие"
        df1 = df1.sort_values(by=['count'])  # сортировка по кол-ву процессов

        users = list(df1.index)
        process_count = list(df1['count'])

        fig = go.Figure(layout={'title': f'Number of Processes vs {choice}'})
        bar = go.Bar(x=users, y=process_count,
                     name=f'Number of Processes vs {choice}')
        fig.add_trace(bar)
        graph_div = offline.plot(fig, auto_open=False, output_type="div")

    return graph_div
