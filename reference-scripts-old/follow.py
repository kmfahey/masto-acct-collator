#!/usr/bin/python3

import sys
import re
import pickle
import pprint
import logging

from mastodon import Mastodon


# LOGGING SETUP

logger_obj = logging.getLogger(name="main")
logger_obj.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: [follow] %(message)s")

handlers = dict(stdout=logging.StreamHandler(sys.stdout),
                file=logging.FileHandler("follow.log", "a"))

for key in ("stdout", "file"):
    handlers[key].setLevel(logging.INFO)
    handlers[key].setFormatter(formatter)
    logger_obj.addHandler(handlers[key])


# LOADING ACCOUNTS TO FOLLOW

accts_to_follow = list()

url_re = re.compile("^https://([^/]+)/(?:.*/)?@?([^/]+)")

with open("accts_to_follow_by_handle.txt", "r") as accts_fh:
    for url in map(str.strip, accts_fh):
        domain, user_id = url_re.match(url).groups()
        accts_to_follow.append(user_id + "@" + domain)

accts_ids_d = {user_id: acct_notifs['favourite']['account']['id']
                            if acct_notifs['favourite'] is not None
                        else acct_notifs['mention']['account']['id']
                            if acct_notifs['mention'] is not None
                        else acct_notifs['reblog']['account']['id']
                            for user_id, acct_notifs in pickle.load(open("notifs_by_acct.dat", "rb")).items()
                                if user_id in accts_to_follow}


# MASTODON CONNECTION

masto = Mastodon(
    client_id=None,
    client_secret=None,
    api_base_url=None,
    ratelimit_method="pace",
)

masto.log_in(
    username="kernefahey@protonmail.com", password="H3g!ouM9QFpO1^Q$", scopes=["read", "write", "follow"]
)

ev_account_d = masto.me()

logger_obj.info(f"got account dict for own account, account id {ev_account_d['id']}")

for user_id, id_ in accts_ids_d.items():
    logger_obj.info(f"following account {user_id}...")
    rel_d = masto.account_follow(id_)
    if rel_d["id"] == id_ and rel_d["following"]:
        logger_obj.info(f"success")
    else:
        logger_obj.warning(f"failure")
