#!/usr/bin/python3

import sys
import re
import pickle
import pprint
import logging
import datetime
import dateutil

from mastodon import Mastodon


masto = Mastodon(
    client_id=None,
    client_secret=None,
    api_base_url=None,
    ratelimit_method="pace",
)

masto.log_in(
    username="kernefahey@protonmail.com", password="H3g!ouM9QFpO1^Q$", scopes=["read", "write", "follow"]
)

print("logged in")

ev_account_d = masto.me()

print("got own account dict")

notifs_page = masto.notifications(types=["follow"])

print(f"got 1st page of notifs: {len(notifs_page)} notifs")

notifs_list = []

threshold_dt = datetime.datetime(2023, 12, 9, 20, 5, 0, 0, dateutil.tz.tz.tzutc())

while notifs_page is not None:
    end_while = False
    for notif in notifs_page:
        if notif['created_at'] < threshold_dt:
            print("advanced in follow notifs list to before 2023-12-09 20:05:00 UTC")
            end_while = True
            break
        else:
            notifs_list.append(notif)
    print(f"got {len(notifs_list)} notifs total")
    if end_while:
        break
    notifs_page = masto.fetch_next(notifs_page)
    print(f"got next page of notifs: {len(notifs_page)} notifs")

notifs_list = list(reversed(notifs_list))

print()
print("followed since mass-follow action:")
print()

for notif in notifs_list:
    print("{display_name}\n<{acct}>".format(**notif['account']), end="\n\n")

print(f"TOTAL RECENT FOLLOWS: {len(notifs_list)}")

pickle.dump(notifs_list, open("own_notifs.dat", "wb"))
