import sqlite3
c = sqlite3.connect('instance/cms.db')
res = c.execute("SELECT id, title, date_added FROM kose_yazisi WHERE date_added LIKE '2026-09-12%'").fetchall()
print(f"Total old articles with 2026-09-12 date: {len(res)}")
print(res[:10])
