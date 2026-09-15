import sqlite3
import csv
from io import StringIO

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
db_path = r'instance/cms.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("DELETE FROM kose_yazisi")

with open(sql_path, 'r', encoding='utf8', errors='ignore') as f:
    text = f.read()

parts = text.split('INSERT INTO `burokratlar_haberkoseyazi`')
print("Found", len(parts) - 1, "INSERT blocks for kose_yazisi")

count = 0
for part in parts[1:]:
    end_idx = part.find(';')
    if end_idx == -1: continue
    
    stmt = part[:end_idx]
    val_idx = stmt.find('VALUES')
    if val_idx == -1: continue
    
    val_str = stmt[val_idx+6:].strip()
    print(repr(val_str[:50]))
    
    tuples = []
    current_tuple = []
    current_val = ""
    in_string = False
    escape = False
    
    for char in val_str:
        if escape:
            current_val += char
            escape = False
        elif char == '\\':
            current_val += char
            escape = True
        elif char == "'":
            in_string = not in_string
        elif char == "," and not in_string:
            current_tuple.append(current_val)
            current_val = ""
        elif char == "(" and not in_string:
            current_tuple = []
            current_val = ""
        elif char == ")" and not in_string:
            current_tuple.append(current_val)
            tuples.append(current_tuple)
            current_val = ""
        else:
            current_val += char
            
    print(current_val[-200:])
    print("in_string:", in_string)
    print("Extracted", len(tuples), "tuples")
    for cols in tuples:
        if len(cols) >= 10:
            try:
                k_id = int(cols[0].strip())
                head = cols[1].strip("'").replace("\\n", "\n").replace("\\'", "'")
                # content is index 8
                info = cols[8].strip("'").replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\'", "'")
                # yazar is index 6
                gid = int(cols[6].strip())
                c.execute("INSERT OR IGNORE INTO kose_yazisi (id, title, content, yazar_id) VALUES (?, ?, ?, ?)",
                          (k_id, head, info, gid))
                count += 1
            except Exception as e:
                pass

conn.commit()
c.execute("SELECT COUNT(*) FROM kose_yazisi")
print("KoseYazisi imported:", c.fetchone()[0])
conn.close()
