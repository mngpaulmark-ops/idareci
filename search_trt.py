import sqlite3
conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()
c.execute("SELECT id, title, status FROM haber WHERE title LIKE '%trt%' COLLATE NOCASE")
for row in c.fetchall():
    print('Haber:', row)

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]

if 'video' in tables:
    c.execute("SELECT id, title, status FROM video WHERE title LIKE '%trt%' COLLATE NOCASE")
    for row in c.fetchall():
        print('Video:', row)
