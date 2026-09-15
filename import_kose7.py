import sqlite3
import csv
from io import StringIO

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
db_path = r'instance/cms.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

count = 0
with open(sql_path, 'r', encoding='utf8', errors='ignore') as f:
    for line in f:
        if line.startswith('INSERT INTO `burokratlar_haberkoseyazi`'):
            idx = line.find('VALUES')
            if idx != -1:
                val_str = line[idx+6:].strip()
                if val_str.endswith(';'): val_str = val_str[:-1]
                if val_str.startswith('('): val_str = val_str[1:]
                if val_str.endswith(')'): val_str = val_str[:-1]
                
                records = val_str.split('),(')
                for rec in records:
                    reader = csv.reader(StringIO(rec), quotechar="'", escapechar='\\')
                    try:
                        cols = next(reader)
                        if len(cols) >= 11:
                            k_id = int(cols[0])
                            head = cols[1]
                            info = cols[7]
                            gid = int(cols[9])
                            c.execute("INSERT OR IGNORE INTO kose_yazisi (id, title, content, yazar_id) VALUES (?, ?, ?, ?)",
                                      (k_id, head, info, gid))
                            count += 1
                    except Exception as e:
                        pass

conn.commit()
c.execute("SELECT COUNT(*) FROM kose_yazisi")
print("KoseYazisi imported:", c.fetchone()[0])
conn.close()
