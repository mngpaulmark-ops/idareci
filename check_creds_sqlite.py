import sqlite3
sl_conn = sqlite3.connect('instance/cms.db')
sl_cur = sl_conn.cursor()
sl_cur.execute("SELECT key, value FROM setting WHERE key IN ('admin_user', 'admin_pass')")
print('Settings in SQLite:', sl_cur.fetchall())

