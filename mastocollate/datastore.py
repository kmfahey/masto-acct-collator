#!/usr/bin/python3

import os
import sqlite3


__export__ = ('DataStore',)

class DataStore:
    db_file_name: str
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, db_file_name) -> None:
        self.db_file_name = db_file_name
        db_existed = os.path.exists(db_file_name)
        self.connection = sqlite3.connect(db_file_name)
        self.cursor = self.connection.cursor()
        if not db_existed:
            self.enable_foreign_keys()
            self.create_profiles_table()
            self.create_profiles_index()
            self.create_profiles_fts_table()
            self.create_notifs_table()
            self.create_follow_table()

    def enable_foreign_keys(self) -> None:
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def create_profiles_table(self) -> None:
        self.cursor.execute(
            """
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
            );"""
        )

    def create_profiles_index(self) -> None:
        self.cursor.execute(
            "CREATE INDEX idx_profiles_fts_rowid ON profiles (fts_rowid);"
        )

    def create_profiles_fts_table(self) -> None:
        self.cursor.execute(
            """
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
            );"""
        )

    def create_notifs_table(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE notifs (
                from_user_id TEXT PRIMARY KEY NOT NULL,
                to_user_id TEXT NOT NULL,
                created_at DATETIME NOT NULL,
                notif_type TEXT NOT NULL,
                status_uri TEXT,
                FOREIGN KEY (from_user_id) REFERENCES profiles(user_id),
                FOREIGN KEY (to_user_id) REFERENCES profiles(user_id)
            );"""
        )

    def create_follow_table(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE follow (
                by_user_id TEXT PRIMARY KEY NOT NULL,
                of_user_id TEXT NOT NULL,
                last_event DATETIME NOT NULL,
                relation TEXT NOT NULL,
                FOREIGN KEY (by_user_id) REFERENCES profiles(user_id),
                FOREIGN KEY (of_user_id) REFERENCES profile(user_id)
            );"""
        )

    def get_last_insert_rowid(self) -> int:
        self.cursor.execute("SELECT last_insert_rowid();")
        (rowid,) = self.cursor.fetchone()
        return rowid

    def update_profiles_w_rowid(self, user_id: str) -> None:
        self.cursor.execute(
            f"""
            UPDATE profiles
            SET fts_rowid = (
                SELECT rowid
                FROM profiles_fts
                WHERE profiles_fts.user_id = {user_id}
            )
            WHERE user_id = {user_id};"""
        )
