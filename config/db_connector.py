import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "jawad_assignments_db.db")

db_conn = sqlite3.connect(DB_PATH, check_same_thread=False)

db_conn.execute("""
           CREATE TABLE IF NOT EXISTS conversations
           (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               app_code TEXT,
               thread_id TEXT,
               role TEXT,
               content TEXT,
               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
           )
           """)

db_conn.commit()

db_conn.execute("""
           CREATE TABLE IF NOT EXISTS thread_list
           (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               thread_id TEXT,
               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
           )
           """)
db_conn.commit()
