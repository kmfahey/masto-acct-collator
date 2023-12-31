#!/usr/bin/python3

import pickle
import logging
import sys
import pprint
from datetime import datetime
from operator import concat
from collections import defaultdict
from mastodon import Mastodon


suffix_to_ordinal = (
    lambda intval: "st"
    if intval % 10 == 1
    else "nd"
    if intval % 10 == 2
    else "rd"
    if intval % 10 == 3
    else "th"
)

VIRAL_POST_ID = None

logger_obj = logging.getLogger(name="main")
logger_obj.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: [notifdler2] %(message)s")

handlers = dict()
handlers["stdout"] = logging.StreamHandler(sys.stdout)
handlers["file"] = logging.FileHandler("notifdler2.log", "a")

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


my_account_d = masto.me()
my_acct_id = my_account_d["id"]
logger_obj.info(f"got account dict for own account, account id {my_acct_id}")
viral_post = masto.status(VIRAL_POST_ID)
logger_obj.info(f"got post dict for viral post (id={VIRAL_POST_ID})")
viral_post_created_at = viral_post['created_at']
logger_obj.info(f"viral post created_at time: {viral_post_created_at.isoformat()}")

followers_handles = set()
followers_page = masto.account_followers(my_acct_id)

while followers_page is not None:
   followers_handles.update(follower_d['username'] for follower_d in followers_page)
   logger_obj.info(f"loaded {len(followers_handles)} followers userids")
   followers_page = masto.fetch_next(followers_page)

notifs_list = list()
notifs_page = masto.notifications(types=["favourite", "reblog", "mention"])
count = 0

no_notifs_pages = 0

while notifs_page is not None:
    break_while_loop = False
    count += 1
    notifs_page = masto.fetch_next(notifs_page)
    notifs_pertaining = 0
    for notif in notifs_page:
        if notif['created_at'] < viral_post_created_at:
            break_while_loop = True
            break
        elif notif["status"]["id"] != None:
            continue
        else:
            notifs_pertaining += 1
            notifs_list.append(notif)
    logger_obj.info(f"got {count}{suffix_to_ordinal(count)} page of notifs_list, length {len(notifs_page)}; found {notifs_pertaining} notifs pertaining to post")
    if break_while_loop:
        logger_obj.info("found notification with created_at date preceding created_at of original post; exiting pagination")
        break

logger_obj.info(f"got {len(notifs_list)} notifications total")

notifs_by_acct_dd = defaultdict(lambda: dict(mention=None, reblog=None, favourite=None))

for notif in notifs_list:
    if notif['account']['acct'] in followers_handles:
       continue
    notifs_by_acct_dd[notif["account"]["acct"]][notif["type"]] = notif

notifs_by_acct = dict(notifs_by_acct_dd)

logger_obj.info(f"found {len(notifs_by_acct)} unique accounts in notifications")

fh = open("notifs_by_acct.dat", "wb")

pickle.dump(notifs_by_acct, fh)
