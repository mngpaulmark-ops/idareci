import sqlite3
import os

db_path = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', 'instance', 'cms.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

try:
    c.execute("ALTER TABLE galeri ADD COLUMN date VARCHAR(50)")
except Exception as e:
    print("Column date might exist:", e)

try:
    c.execute("ALTER TABLE galeri ADD COLUMN location VARCHAR(100)")
except Exception as e:
    print("Column location might exist:", e)

conn.commit()
conn.close()
print("Added date and location to galeri table.")
