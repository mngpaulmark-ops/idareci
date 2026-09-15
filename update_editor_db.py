import sqlite3
import os

db_path = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', 'instance', 'cms.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

try:
    c.execute("ALTER TABLE editor_user ADD COLUMN can_galeri BOOLEAN DEFAULT 0")
except Exception as e:
    print("can_galeri column might already exist:", e)

try:
    c.execute("ALTER TABLE editor_user ADD COLUMN can_video BOOLEAN DEFAULT 0")
except Exception as e:
    print("can_video column might already exist:", e)

conn.commit()
conn.close()
print("Added can_galeri and can_video to editor_user table.")
