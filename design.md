# Disparate Script Files

The script files I wrote while trying to solve a series of related problems via the Mastodon API, using the python Mastodon module, and the purpose of each script, are listed below.

| Script | Functionality
| ------ | -------------
| datscan.py | takes .dat file produced by notifdler and commits it to an SQL database
| flwr\_query.py | an experiment with trying to download the followers of an account at another host
| follow.py | takes a list of accounts and follows each user
| notifdler2.py | given a specific post id belonging to the logging-in user, loads all notifications pertaining to that post, and saves the full dict-of-dicts of notifications to a .dat file using pickle
| notifdler.py | given a specific post id belonging to the logging-in user, loads all notifications pertaining to that post until a specific notification is encountered, saves the full dict-of-dicts of notifications to a .dat file using pickle
| notif\_list\_rearranger.py | postprocessor that loads the .dat file created by notifdler or notifdler2, rearranges it and saves the result to a different .dat file
| recent\_follows.py | downloads recent follow notifications emitted after a certain point in the past, and displays them
| search2.py | downloads the followers and following user lists and saves them to a .dat file
| search3.py | runs down a list of search terms and iteratively matches each one against a MySQL table of masto account data that has FULLTEXT set up, then displays all the matching account data in a justified table
| search4.py | as search3 but with a much shorter list
| search.py | as search3 but an earlier iteration of the same functionality

# Important Mastodon API v1 Incantation

If one has the handle of a randomly select mastodon user, and wishes to programmatically download their followers and following lists, the following functionality *may* work.

1. Break down the handle into the values `$USERNAME` and `$INSTANCE` derived from that handle.
1. Attempt to load the REST url `https://$INSTANCE/api/v1/accounts/lookup?acct=$USERNAME`
1. If the result was a non-200 status code, or output of the form `{"error":"Record not found"}`, this will not work.
1. Otherwise, from the JSON object that results, access the property `id` and store the value (here, as `$ID`).
1. Followers and following can now be reached via the v1 API under the REST url `https://$INSTANCE/api/v1/accounts/$ID`
    * Followers will be accessible at the REST url `https://$INSTANCE/api/v1/accounts/$ID/followers`
    * Followings will be accessible at the REST url `https://$INSTANCE/api/v1/accounts/$ID/following`
    * Refer to the Link header of the response for pagination links to prev and next pages

This functionality is not supported on all servers. It worked when tried on mastodon.social, lea.pet, and mas.to. It did not work on cybre.space. At the time of writing the author does not know whether it normally requires the client to be logged-in to the instance. Since mastodon.social is in many respects the canonical mastodon instance, and that instance doesn't require a login to use this functionality, that is *likely* to be the default.

# Proposed and Possible Script Functionality

* Create & maintain an on-disk database (sqlite3).

* Download the followers and followings associated with the logging-in user's account. (And store them in the sqlite3 db.)

* Given a list of accounts, follow each one via the logged-in user's account.

* Given a specific post id belonging to the logged-in user, load all notifications pertaining to that post. (Store in them in the db.)
    * Differentiate from the account dicts included in each Mastodon.py response. (Store those in the db too.)

* Download recent follow notifications up to a certain point in the past. (Save them to the db.) And display them.

* Compare current followers list to most recent copy and detect unfollows.

* Given a list of search terms, iteratively matches each one against the FULLTEXT index of the sqlite3 table of profiles and displays matches.

# SQLite3 Table Schema Brainstorming

* profiles

    * Have a handle column. Useful as a single-column foreign key.

    * Use handle as primary key? Or have a normal autoincrementing numeric id?

    * Also store the profile(s) of any logged-in user in the same table?

        * Use special flag to denote profiles of this kind?

    * Column for every single property in the account JSON object?
    
        * Or should we disregard all the known-irrelevant properties and conform to the schema of the MySQL table current serving this purpose?

* notifs

    * Foreign key (`handle`) to profiles table.

* follow_ers_ings

    * Foreign `handle` key <= profiles table to the user's profile

    * Foreign `handle` key <= profiles table to login-able has-a user profile

    * One table, with a ternary pseudo-enum column denoting follower, following, or mutual.

    * ⊘ No need to have two identical tables differing only in semantic significance of the table names. ⊘ 


