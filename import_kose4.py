import sqlite3
import re

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
db_path = r'instance/cms.db'

with open(sql_path, 'r', encoding='utf8', errors='ignore') as f:
    sql_text = f.read()

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("DELETE FROM kose_yazisi")

# We will read character by character to safely extract tuples
matches = re.finditer(r'INSERT INTO `burokratlar_haberkoseyazi` \([^)]+\) VALUES (.*?);', sql_text, re.DOTALL)
for match in matches:
    values_str = match.group(1)
    
    tuples = []
    in_string = False
    escape = False
    current_tuple = []
    current_val = ""
    
    for char in values_str:
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
            
    for cols in tuples:
        if len(cols) >= 11:
            try:
                k_id = int(cols[0])
                head = cols[1]
                info = cols[7].replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\'", "'")
                gid = int(cols[9])
                c.execute("INSERT INTO kose_yazisi (id, title, content, yazar_id) VALUES (?, ?, ?, ?)",
                          (k_id, head, info, gid))
            except Exception as e:
                print("Error on tuple:", cols[0], e)

conn.commit()
c.execute("SELECT COUNT(*) FROM kose_yazisi")
print("KoseYazisi imported:", c.fetchone()[0])
conn.close()
