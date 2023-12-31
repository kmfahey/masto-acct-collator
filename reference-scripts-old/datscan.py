#!/usr/bin/python3

import MySQLdb
import pprint
import pickle
import functools
import collections
import html2text


connection = MySQLdb.Connect(user=None, password=None, host="localhost", database="mst_acct_recdr", charset="utf8mb4")
cursor = connection.cursor()

#escape = lambda strval: '"{strval}"'.format(strval=str(strval).translate({0: '\x00', 8: '\\b', 9: '\\t', 10: '\\n', 13: '\\r', 26: '\\Z', 34: '\\"', 37: '\\%', 39: "\\'", 92: '\\\\', 95: '\\_'}))

fh = open("notifs_by_acct.dat", "rb")

dat = pickle.load(fh)

cursor.execute("SELECT user_id FROM profiles;")
user_ids_in_table = {row[0] for row in cursor.fetchall()};

might_have_html_in = lambda strval: '<' in strval and '>' in strval

for notif_triple in dat.values():
    notif_dts = list()
    account_d = dict()

    for ntype in ('favourite', 'reblog', 'mention'):
        if notif_triple[ntype] is None:
            continue
        notif = notif_triple[ntype]
        notif_dts.append(notif['created_at'])
        account_d.update(notif['account'])

    if account_d['acct'] in user_ids_in_table:
        continue

    fields_len = len(account_d['fields']) if 'fields' in account_d else 0

    db_row_d = {
        'acct_id': account_d['id'],
        'user_id': account_d['acct'],
        'user_name': account_d['username'],
        'url': account_d['url'],
        'field_name_1': html2text.html2text(str(account_d['fields'][0]['name'])) if fields_len >= 1 else "NULL",
        'field_value_1': html2text.html2text(str(account_d['fields'][0]['value'])) if fields_len >= 1 else "NULL",
        'field_name_2': html2text.html2text(str(account_d['fields'][1]['name'])) if fields_len >= 2 else "NULL",
        'field_value_2': html2text.html2text(str(account_d['fields'][1]['value'])) if fields_len >= 2 else "NULL",
        'field_name_3': html2text.html2text(str(account_d['fields'][2]['name'])) if fields_len >= 3 else "NULL",
        'field_value_3': html2text.html2text(str(account_d['fields'][2]['value'])) if fields_len >= 3 else "NULL",
        'field_name_4': html2text.html2text(str(account_d['fields'][3]['name'])) if fields_len >= 4 else "NULL",
        'field_value_4': html2text.html2text(str(account_d['fields'][3]['value'])) if fields_len >= 4 else "NULL",
        'text': html2text.html2text(str(account_d['note'])),
        'earliest_notif_ts': sorted(notif_dts)[0].strftime("%Y-%m-%d %H:%M:%S"),
        'tested': 0
    }

    sql_statement = """INSERT INTO profiles
                           (
                               `acct_id`, `user_id`, `user_name`, `url`,
                               `field_name_1`, `field_value_1`, `field_name_2`,
                               `field_value_2`, `field_name_3`, `field_value_3`,
                               `field_name_4`, `field_value_4`, `text`,
                               `earliest_notif_ts`, `tested`
                           ) VALUES (
                               %(acct_id)s, %(user_id)s, %(user_name)s,
                               %(url)s, %(field_name_1)s, %(field_value_1)s,
                               %(field_name_2)s, %(field_value_2)s, %(field_name_3)s,
                               %(field_value_3)s, %(field_name_4)s,
                               %(field_value_4)s, %(text)s, %(earliest_notif_ts)s,
                               %(tested)s
                           );
                    """

    cursor.execute(sql_statement, db_row_d)
    connection.commit()

    print(f"added info for acct_id {db_row_d['acct_id']}, user_id {db_row_d['user_id']}")
