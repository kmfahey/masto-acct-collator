# Disparate Script Files

The script files I wrote while trying to solve a series of related problems via the Mastodon API, using the python Mastodon module, and the purpose of each script, are listed below.

| Script | Functionality |
| ------ | ------------- |
| datscan.py | takes .dat file produced by notifdler and commits it to an SQL database |
| flwr\_query.py | an experiment with trying to download the followers of an account at another host |
| follow.py | takes a list of accounts and follows each user |
| notifdler2.py | given a specific post id belonging to the logging-in user, loads all notifications pertaining to that post, and saves the full dict-of-dicts of notifications to a .dat file using pickle |
| notifdler.py | given a specific post id belonging to the logging-in user, loads all notifications pertaining to that post until a specific notification is encountered, saves the full dict-of-dicts of notifications to a .dat file using pickle |
| notif\_list\_rearranger.py | postprocessor that loads the .dat file created by notifdler or notifdler2, rearranges it and saves the result to a different .dat file |
| recent\_follows.py | downloads recent follow notifications emitted after a certain point in the past, and displays them |
| search2.py | downloads the followers and following user lists and saves them to a .dat file |
| search3.py | runs down a list of search terms and iteratively matches each one against a MySQL table of masto account data that has FULLTEXT set up, then displays all the matching account data in a justified table |
| search4.py | as search3 but with a much shorter list |
| search.py | as search3 but an earlier iteration of the same functionality |
