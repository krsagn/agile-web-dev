import os
import sqlite3
from datetime import datetime, timezone

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(app):
    os.makedirs(app.instance_path, exist_ok=True)

    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS login_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS registered_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                terms_read TEXT NOT NULL DEFAULT 'no',
                created_at TEXT NOT NULL
            )
            """
        )
        db.commit()

    app.teardown_appcontext(close_db)


def save_login_credentials(username, password_hash):
    created_at = datetime.now(timezone.utc).isoformat()
    db = get_db()
    db.execute(
        """
        INSERT INTO login_credentials (username, password_hash, created_at)
        VALUES (?, ?, ?)
        """,
        (username, password_hash, created_at),
    )
    db.commit()


def save_registered_user(first_name, last_name, email, username, password_hash, terms_read):
    created_at = datetime.now(timezone.utc).isoformat()
    db = get_db()
    db.execute(
        """
        INSERT INTO registered_users (
            first_name,
            last_name,
            email,
            username,
            password_hash,
            terms_read,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (first_name, last_name, email, username, password_hash, terms_read, created_at),
    )
    db.commit()
