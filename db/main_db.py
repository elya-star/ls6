import sqlite3
from config import path_db


def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        date TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def add_task(task):
    from datetime import datetime

    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    date_now = datetime.now().strftime("%d.%m.%Y %H:%M")

    cursor.execute(
        "INSERT INTO tasks (task, date) VALUES (?, ?)",
        (task, date_now)
    )

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id, date_now

def delete_task(task_id: int):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id, ))
    conn.commit()
    conn.close()

