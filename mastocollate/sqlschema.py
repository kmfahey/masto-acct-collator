#!/usr/bin/python3

__export__ = ("FOREIGN_KEYS_PRAGMA_SQL", "PROFILES_CREATE_TABLE_SQL", "PROFILES_CREATE_INDEX_SQL", "PROFILES_FTS_CREATE_TABLE_SQL", "NOTIFS_CREATE_TABLE_SQL", "FOLLOW_CREATE_TABLE_SQL")


FOREIGN_KEYS_PRAGMA_SQL = """
PRAGMA foreign_keys = ON;
"""

PROFILES_CREATE_TABLE_SQL = """
CREATE TABLE profiles (
    user_id TEXT PRIMARY KEY NOT NULL,
    fts_rowid INT,
    acct_id INT NOT NULL,
    user_name TEXT NOT NULL,
    instance TEXT NOT NULL,
    uri TEXT NOT NULL,
    field_name_1 TEXT,
    field_value_1 TEXT,
    field_name_2 TEXT,
    field_value_2 TEXT,
    field_name_3 TEXT,
    field_value_3 TEXT,
    field_name_4 TEXT,
    field_value_4 TEXT,
    profile_text TEXT NOT NULL,
    earliest_notif DATETIME NOT NULL,
    loginable BOOLEAN NOT NULL,
    tested BOOLEAN NOT NULL
);
"""

PROFILES_CREATE_INDEX_SQL = """
CREATE INDEX idx_profiles_fts_rowid ON profiles (fts_rowid);
"""

PROFILES_FTS_CREATE_TABLE_SQL = """
CREATE VIRTUAL TABLE profiles_fts USING fts5(
    user_id,
    user_name,
    instance,
    field_name_1,
    field_value_1,
    field_name_2,
    field_value_2,
    field_name_3,
    field_value_3,
    field_name_4,
    field_value_4,
    profile_text
);
"""

NOTIFS_CREATE_TABLE_SQL = """
CREATE TABLE notifs (
    from_user_id TEXT PRIMARY KEY NOT NULL,
    to_user_id TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    notif_type TEXT NOT NULL,
    status_uri TEXT,
    FOREIGN KEY (from_user_id) REFERENCES profiles(user_id),
    FOREIGN KEY (to_user_id) REFERENCES profiles(user_id)
);
"""

FOLLOW_CREATE_TABLE_SQL = """
CREATE TABLE follow (
    by_user_id TEXT PRIMARY KEY NOT NULL,
    of_user_id TEXT NOT NULL,
    last_event DATETIME NOT NULL,
    relation TEXT NOT NULL,
    FOREIGN KEY (by_user_id) REFERENCES profiles(user_id),
    FOREIGN KEY (of_user_id) REFERENCES profile(user_id)
);
"""

# LAST_ROWID_SELECT_STATEMENT = "SELECT last_insert_rowid();"
