import sqlite3
import os

db_path = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', 'instance', 'cms.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

updates = {
    1: {"date": "16 Haziran 2016", "location": "Ankara"},
    2: {"date": "16 Haziran 2016", "location": "Ankara"},
    5: {"date": "19 Ağustos 2017", "location": "Hakkari"},
    6: {"date": "", "location": ""},
    7: {"date": "23 Kasım 2017", "location": "Ankara"},
    8: {"date": "18 Aralık 2017", "location": "Ankara"},
    9: {"date": "06 Haziran 2018", "location": "Ankara"}
}

for gid, data in updates.items():
    c.execute("UPDATE galeri SET date=?, location=? WHERE id=?", (data["date"], data["location"], gid))

conn.commit()
conn.close()
print("Updated galeri DB with accurate date and location!")
