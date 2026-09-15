import sqlite3
conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()
c.execute("SELECT * FROM menu WHERE title LIKE '%trt%' COLLATE NOCASE")
print('Menu:', c.fetchall())

c.execute("SELECT id, title FROM haber WHERE title LIKE '%trt%' COLLATE NOCASE")
for row in c.fetchall():
    print('Haber:', row)
