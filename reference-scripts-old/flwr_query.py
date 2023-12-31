#!/usr/bin/python3

import pprint
import pickle
import logging
import sys
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


logger_obj = logging.getLogger(name="main")
logger_obj.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: [flwr_query] %(message)s")

handlers = dict()
handlers["stdout"] = logging.StreamHandler(sys.stdout)
handlers["file"] = logging.FileHandler("flwr_query.log", "a")

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
my_acct_id = my_account_d['id']
logger_obj.info(f"got account dict for own account, account id {my_acct_id}")

#for method, flw_category in ((Mastodon.account_following, "following"),
#                             (Mastodon.account_followers, "followers")):
#    follow_accts = set()
#    follow_page = method(masto, my_acct_id)
#
#    while follow_page is not None:
#        follow_accts.update(follow_d['acct'] for follow_d in follow_page)
#        logger_obj.info(f"loaded {len(follow_accts)} {flw_category} accts")
#        follow_page = masto.fetch_next(follow_page)
#
#    pickle.dump(follow_accts, open(f"{flw_category}.dat", "wb"))


results = masto.search("@HTHR@cybre.space", resolve=True, result_type="accounts")

accounts = results['accounts']

logger_obj.info(f"searched for @HTHR@cybre.space, got {len(accounts)} results")

hthr_acct_id = accounts[0]['id']

hthr_flwrs = masto.account_followers(hthr_acct_id)

logger_obj.info(f"got {len(hthr_flwrs)} followers for @HTHR@cybre.space")

hthr_flwng = masto.account_following(hthr_acct_id)

logger_obj.info(f"got {len(hthr_flwng)} following for @HTHR@cybre.space")




