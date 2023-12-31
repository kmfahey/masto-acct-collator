#!/usr/bin/python3

import pickle

from collections import defaultdict


fh = open("notifs.dat", "rb")

dat = pickle.load(fh)

fh.close()

notifs_by_acct = defaultdict(lambda: dict(mention=None, reblog=None, favourite=None))

for notif in dat:
    notif_type = notif['type']
    notif_acct = notif['account']['acct']
    print(f"filed {notif_type} by {notif_acct}")
    notifs_by_acct[notif_acct][notif_type] = notif

notifs_by_acct = dict(notifs_by_acct)

fh = open("notifs_by_acct.dat", "wb")

pickle.dump(notifs_by_acct, fh)


