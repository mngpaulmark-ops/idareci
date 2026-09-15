import sqlite3
conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()

# Reset admin_pass to plain text '123456'
c.execute("UPDATE setting SET value = '123456' WHERE key = 'admin_pass'")

# Make sure admin_user exists
c.execute("SELECT COUNT(*) FROM setting WHERE key = 'admin_user'")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO setting (key, value) VALUES ('admin_user', 'admin')")
else:
    c.execute("UPDATE setting SET value = 'admin' WHERE key = 'admin_user'")

conn.commit()

# Verify
c.execute("SELECT key, value FROM setting WHERE key IN ('admin_user', 'admin_pass')")
print("Updated credentials:", c.fetchall())
conn.close()
