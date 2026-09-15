import sqlite3
c = sqlite3.connect('instance/cms.db')
print(c.execute("SELECT date_added, title FROM kose_yazisi WHERE date_added > '2026-09-13'").fetchall())
