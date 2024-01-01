# Disparate Script Files

The script files I wrote while trying to solve a series of related problems via the Mastodon API, using the python Mastodon module, and the purpose of each script, are listed below.

| Script                     | Functionality                                                                                                                                                                                                                      |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `datscan.py`               | takes .dat file produced by notifdler and commits it to an SQL database                                                                                                                                                            |
| `flwr_query.py`            | an experiment with trying to download the followers of an account at another host                                                                                                                                                  |
| `follow.py`                | takes a list of accounts and follows each user                                                                                                                                                                                     |
| `notifdler2.py`            | given a specific post id belonging to the logging-in user, loads all notifications pertaining to that post, and saves the full dict-of-dicts of notifications to a .dat file using pickle                                          |
| `notifdler.py`             | given a specific post id belonging to the logging-in user, loads all notifications pertaining to that post until a specific notification is encountered, saves the full dict-of-dicts of notifications to a .dat file using pickle |
| `notif_list_rearranger.py` | postprocessor that loads the .dat file created by notifdler or notifdler2, rearranges it and saves the result to a different .dat file                                                                                             |
| `recent_follows.py`        | downloads recent follow notifications emitted after a certain point in the past, and displays them                                                                                                                                 |
| `search2.py`               | downloads the followers and following user lists and saves them to a .dat file                                                                                                                                                     |
| `search3.py`               | runs down a list of search terms and iteratively matches each one against a MySQL table of masto account data that has FULLTEXT set up, then displays all the matching account data in a justified table                           |
| `search4.py`               | as search3 but with a much shorter list                                                                                                                                                                                            |
| `search.py`                | as search3 but an earlier iteration of the same functionality                                                                                                                                                                      |

# Important Mastodon API v1 Incantation

If one has the handle of a randomly select mastodon user, and wishes to programmatically download their followers and following lists, the following procedure *may* work.

1. Break down the handle into the values `$USERNAME` and `$INSTANCE` derived from that handle.
1. Attempt to load the REST url `https://$INSTANCE/api/v1/accounts/lookup?acct=$USERNAME`
1. If the result was a non-200 status code, or output of the form `{"error":"Record not found"}`, this will not work.
1. Otherwise, from the JSON object that results, access the property `id` and store the value (here, as `$ID`).
1. Followers and following can now be reached via the v1 API under the REST url `https://$INSTANCE/api/v1/accounts/$ID`
    * Followers will be accessible at the REST url `https://$INSTANCE/api/v1/accounts/$ID/followers`
    * Followings will be accessible at the REST url `https://$INSTANCE/api/v1/accounts/$ID/following`
    * Refer to the Link header of the response for pagination links to prev and next pages

This functionality is not supported on all servers. It worked when tried on `mastodon.social`, `lea.pet`, and `mas.to`. It did not work when tried on `cybre.space`. At the time of writing the author does not know whether it normally requires the client to be logged-in to the instance. Since `mastodon.social` is in many respects the canonical mastodon instance, and that instance doesn't require a login to use this functionality, that is *likely* to be the default.

# Proposed and Possible Script Functionality

* Create & maintain an on-disk database (`sqlite3`).

* Download the followers, followings, and follow-requested accounts associated with the logging-in user's account. (And store them in the db.)

* Given a list of accounts, follow each one via the logged-in user's account. (And update the `follow` table accordingly.)

* Given a specific post id belonging to the logged-in user, load all notifications pertaining to that post. (And store in them in the db.)

    * Pull out the account dicts included in each Mastodon.py response. (Store those in the db too.)

* Download recent follow notifications up to a certain point in the past, and display them. (Also save them to the db.)

* Compare current followers list to most recent copy and detect unfollows. (Update the `follow` table.)

* Given a list of search terms, iteratively matches each one against the FULLTEXT index of the sqlite3 table of profiles and displays matches.

# SQLite3 Table Schema First Draft

* `profiles` table:

    * `handle` column: Text. Primary key.

        * A text primary key is less efficient than a numeric one. But the data in the table is more human-readable, which is relevant since the author is known to muck about at the SQL command prompt.

    * `loginable` column: boolean, indicates the profile is of a user who has been logged-in as at least once.

    * As a starting point, should be based on the same schema as the MySQL table currently serving this purpose. What follows is the schema as translated to SQLite 3.40 by [jooq.org](https://www.jooq.org/):

```
CREATE TABLE profiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  acct_id INT8 NOT NULL,
  user_id CLOB NOT NULL,
  user_name CLOB NOT NULL,
  url CLOB NOT NULL,
  field_name_1 CLOB,
  field_value_1 CLOB,
  field_name_2 CLOB,
  field_value_2 CLOB,
  field_name_3 CLOB,
  field_value_3 CLOB,
  field_name_4 CLOB,
  field_value_4 CLOB,
  profile_text CLOB NOT NULL,
  earliest_notif_ts DATETIME NOT NULL,
  tested TINYINT NOT NULL DEFAULT ('0'),
  INDEX user_id (user_id),
  INDEX header_value_1 (field_value_1),
  INDEX header_value_2 (field_value_2),
  INDEX header_value_3 (field_value_3),
  INDEX header_value_4 (field_value_4),
  INDEX profile_text (text),
  INDEX user_name (user_name)
)
ENGINE InnoDB
AUTO_INCREMENT 1
DEFAULT CHARSET utf8mb4
COLLATE utf8mb4_0900_ai_ci
```

* `notifs` table:

    * `notifier_handle` column: foreign key <= profiles table to initiating user's profile

    * `type` column => pseudo-enum: "mention", "favourite", "reblog", "follow"

    * `uri` column: text

        * Both `uri` and `url` properties are included in the JSON object. Notionally the `uri` property should be more authoritative than the `url` property. In practice this may or may not be the case.

* `follow` table:

    * `user_handle` column: Foreign key <= profiles table to follower/following/mutual user's profile

    * `owning_handle` column: Foreign key <= profiles table to login-able has-a user profile

    * `relation` column: a pseudo-enum: "follower", "following", "mutual", "requested", "no-longer-following", "no-longer-follower", "no-longer-mutual"

    * ⊘ No need to have two identical tables differing only in semantic significance of the table names. ⊘ 


