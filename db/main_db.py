import sqlite3
from db import queries
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

def update_task(task_id, new_task=None, completed=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if new_task is not None:
        cursor.execute(queries.update_task, (new_task, task_id))
    elif completed is not None:
        cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (completed, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id: int):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id, ))
    conn.commit()
    conn.close()



def get_tasks(filter_type):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if filter_type == 'all':
        cursor.execute(queries.select_task)
    elif filter_type == 'completed':
        cursor.execute(queries.select_task_completed)
    elif filter_type == 'uncompleted':
        cursor.execute(queries.select_task_uncompleted)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_completed_tasks():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.delete_task_completed)
    conn.commit()
    conn.close()
