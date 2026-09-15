import sqlite3
c = sqlite3.connect('instance/cms.db')
res = c.execute("SELECT date_added, title FROM kose_yazisi WHERE date_added < '2026-09-12' ORDER BY date_added DESC LIMIT 5").fetchall()
for r in res: print(r)
