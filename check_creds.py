import sqlite3
conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()
c.execute("SELECT key, value FROM setting")
rows = c.fetchall()
print('All settings:', rows)
conn.close()
