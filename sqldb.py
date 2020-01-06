import sqlite3

conn = sqlite3.connect('base_score.db')

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     name TEXT,
     score INTEGER
)
""")

conn.commit()

