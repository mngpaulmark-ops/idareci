import sqlite3
conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()
for t in tables:
    c.execute(f"SELECT count(*) FROM {t[0]}")
    print(t[0], ':', c.fetchone()[0])
