import sqlite3
from flask import g

from config import Config

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(Config.DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

def execute_query(query, args=(), one=False):
    try:
        conn = get_db()
        cur = conn.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        conn.commit()
        return (rv[0] if rv else None) if one else rv
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None