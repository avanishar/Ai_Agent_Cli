import sqlite3
import datetime
from pathlib import Path

DB_PATH = Path("history.db")

def _conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS generations (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                type     TEXT NOT NULL,
                topic    TEXT NOT NULL,
                filename TEXT NOT NULL,
                created  TEXT NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS chat_logs (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                role    TEXT NOT NULL,
                message TEXT NOT NULL,
                created TEXT NOT NULL
            )
        """)

def log_generation(type_: str, topic: str, filename: str):
    with _conn() as con:
        con.execute(
            "INSERT INTO generations (type, topic, filename, created) VALUES (?,?,?,?)",
            (type_, topic, filename, datetime.datetime.now().isoformat(timespec="seconds"))
        )

def log_chat(role: str, message: str):
    with _conn() as con:
        con.execute(
            "INSERT INTO chat_logs (role, message, created) VALUES (?,?,?)",
            (role, message, datetime.datetime.now().isoformat(timespec="seconds"))
        )

def get_history(limit=20) -> list[dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT id, type, topic, filename, created FROM generations ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [{"id": r[0], "type": r[1], "topic": r[2], "filename": r[3], "created": r[4]} for r in rows]

def clear_history():
    with _conn() as con:
        con.execute("DELETE FROM generations")
        con.execute("DELETE FROM chat_logs")
