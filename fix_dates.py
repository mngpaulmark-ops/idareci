import sqlite3

conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()
c.execute("UPDATE kose_yazisi SET date_added = '2000-01-01 00:00:00' WHERE date_added LIKE '2026-09-12 17:29:48%'")
conn.commit()
conn.close()

print("Updated dates for old bulk articles.")
