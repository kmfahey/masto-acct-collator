#!/usr/bin/python3

import pickle
import MySQLdb


# VARIABLES & CONNECTION SETUP

terms = ['"non-binary"', 'enby', 'nb', 'nonbinary',

         '"trans fem"', '"trans femm"', '"trans femme"', '"trans girl"',
         '"trans woman"', 'transbian', 'transgirl', 'transwoman', 'transfem',
         'transfemm', 'transfemme',

         'sapphic', 'lesbian', 'gay', 'mlm', 'wlw',

         '"trans guy"', '"trans man"', '"trans masc"', 'transguy', 'transman',
         'transmasc',

         'aromantic', 'aro', 'asexual', 'ace', 'aroace', '"grey-ace"',
         'grayace', 'greyace', '"gray ace"', '"grey ace"', '"gray-ace"',
         'graysexual',

         'demiguy', 'demigirl', '"demi-guy"', '"demi-girl"', 'demisexual',

         'androphilia', 'androsexual', 'gynephilia', 'gynosexual',

         'homo', 'homosexual',

         'bi', 'bisexual', 'bicurious', '"bi-curious"', 'biromantic', 'panromantic',
         'panromantic',

         'pan', 'pansexual', 'panromantic',

         'cupiosexual', 'grayromantic', 'omnisexual', 'omniromantic',
         'polysexual', 'skoliosexual', 'lithosexual', 'akoiosexual',
         'spectrasexual',

         'queer']

fields = ["user_id", "field_value_1", "field_value_2", "field_value_3",
          "field_value_4", "text", "user_name"]

connection = MySQLdb.Connect(user=None, password=None, host="localhost", database="mst_acct_recdr", charset="utf8mb4")
cursor = connection.cursor()

userids_follow_ing_ers = set(pickle.load(open("followers.dat", "rb"))) & set(pickle.load(open("following.dat", "rb")))


cursor.execute("SELECT MAX(earliest_notif_ts) FROM profiles;")
((earliest_notif_ts,),) = cursor.fetchall()

# DATA COLLECTION

result_rows = set()

for term in terms:
    fulltext_clause = " OR ".join("MATCH({field}) AGAINST('{term}'{mode})".format(field=field, term=term, mode=" IN BOOLEAN MODE" if field != "user_id" else "") for field in fields)
    rows_affected = cursor.execute(f"SELECT id, acct_id, user_id, user_name, url FROM profiles WHERE {fulltext_clause};")
    result_rows.update(tuple(map(str, row)) for row in cursor.fetchall())
    #print(f"added {rows_affected} rows_affected for search against {term}")
    #print(f"running total rows_affected = {len(result_rows)}")

result_rows = list(filter(lambda row: row[2] not in userids_follow_ing_ers, result_rows))

#print(f"reduced total rows to {len(result_rows)} after filtering out known followers/ing user_ids")


# OUTPUT FORMATTING

max_id_width = 0
max_acct_id_width = 0
max_user_id_width = 0
max_user_name_width = 0
max_url_width = 0

for id_, acct_id, user_id, user_name, url in result_rows:
    id_ = str(id_)
    acct_id = str(acct_id)
    if len(id_) > max_id_width:
        max_id_width = len(id_)
    if len(acct_id) > max_acct_id_width:
        max_acct_id_width = len(acct_id)
    if len(user_id) > max_user_id_width:
        max_user_id_width = len(user_id)
    if len(user_name) > max_user_name_width:
        max_user_name_width = len(user_name)
    if len(url) > max_url_width:
        max_url_width = len(url)

separator = "+-" + (max_id_width * "-") + "-+-" + (max_acct_id_width * "-") + "-+-" + (max_user_id_width * "-") + "-+-" + (max_user_name_width * "-") + "-+-" + (max_url_width * "-") + "-+"

row_str_w_padding = lambda id_, acct_id, user_id, user_name, url: "| " + " | ".join((id_.ljust(max_id_width),
                                                                                     acct_id.ljust(max_acct_id_width),
                                                                                     user_id.ljust(max_user_id_width),
                                                                                     user_name.ljust(max_user_name_width),
                                                                                     url.ljust(max_url_width))) + " |"

print(separator)
print(row_str_w_padding("id", "acct_id", "user_id", "user_name", "url"))
print(separator)

for id_, acct_id, user_id, user_name, url in result_rows:
    print(row_str_w_padding(id_, acct_id, user_id, user_name, url))

print(separator)
print()
print("MAX(earliest_notif_ts) in UTC:")
print(earliest_notif_ts.isoformat())

