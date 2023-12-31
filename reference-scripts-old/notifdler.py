#!/usr/bin/python3

import pickle
import logging
import sys

from collections import defaultdict
from mastodon import Mastodon


logger_obj = logging.getLogger(name="main")
logger_obj.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")

handlers = dict()
handlers["stdout"] = logging.StreamHandler(sys.stdout)
handlers["file"] = logging.FileHandler("notifdler.log", "a")

for key in ("stdout", "file"):
    handlers[key].setLevel(logging.INFO)
    handlers[key].setFormatter(formatter)
    logger_obj.addHandler(handlers[key])


masto = Mastodon(
    client_id=None,
    client_secret=None,
    api_base_url=None,
    ratelimit_method="pace",
)

masto.log_in(
    username="kernefahey@protonmail.com", password="H3g!ouM9QFpO1^Q$", scopes=["read"]
)


ev_account_d = masto.me()

logger_obj.info(f"got account dict for own account, account id {ev_account_d['id']}")

suffix_to_ordinal = (
    lambda intval: "st"
    if intval % 10 == 1
    else "nd"
    if intval % 10 == 2
    else "rd"
    if intval % 10 == 3
    else "th"
)

notifs_list = list()

notifs_page = masto.notifications(types=["favourite", "reblog", "mention"])

count = 0

is_kittens_houses_fav = (
    lambda notif: notif["status"]["uri"].endswith("111526626889798911")
    and notif["account"]["acct"] == "kittenshouse@pounced-on.me"
)

while notifs_page is not None:
    count += 1
    logger_obj.info(
        f"got {count}{suffix_to_ordinal(count)} page of notifs_list, length {len(notifs_page)}"
    )
    notifs_page = masto.fetch_next(notifs_page)
    if any(is_kittens_houses_fav(notif) for notif in notifs_page):
        for notif in notifs_page:
            notifs_list.append(notif)
            if is_kittens_houses_fav(notif):
                logger_obj.info(
                    "found Kitten's House System's fav of post id 111526626889798911"
                )
                break
        break
    else:
        notifs_list.extend(notifs_page)

logger_obj.info(
    f"got {len(notifs_list)} notifications since Kitten's House System's fav (inclusive)"
)

# logger_obj.info(f"storing notifs_list list, length {len(notifs_list)}")
#
# with open("notifs.dat", "wb") as notifs_fh:
#    pickle.dump(notifs_list, notifs_fh)

notifs_by_acct_dd = defaultdict(lambda: dict(mention=None, reblog=None, favourite=None))

for notif in notifs_list:
    notif_type = notif["type"]
    notif_acct = notif["account"]["acct"]
    # logger_obj.info(f"filed {notif_type} by {notif_acct}")
    notifs_by_acct_dd[notif_acct][notif_type] = notif

notifs_by_acct = dict(notifs_by_acct_dd)

logger_obj.info(f"found {len(notifs_by_acct)} unique accounts in notifications")

fh = open("notifs_by_acct.dat", "wb")

pickle.dump(notifs_by_acct, fh)
