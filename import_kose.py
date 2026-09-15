import sqlite3
import re

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
db_path = r'instance/cms.db'

with open(sql_path, 'r', encoding='utf8', errors='ignore') as f:
    sql_text = f.read()

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("DELETE FROM yazar")
c.execute("DELETE FROM kose_yazisi")

match_group = re.search(r'INSERT INTO `burokratlar_haberkosegroup` \([^)]+\) VALUES (.*?);', sql_text, re.DOTALL)
if match_group:
    values_str = match_group.group(1)
    records = values_str.split("),(")
    for rec in records:
        rec = rec.strip("()")
        cols = []
        in_quote = False
        current = ""
        for char in rec:
            if char == "'":
                in_quote = not in_quote
            elif char == "," and not in_quote:
                cols.append(current)
                current = ""
                continue
            current += char
        cols.append(current)
        
        try:
            y_id = int(cols[0])
            name = cols[1].strip("'")
            pic = cols[5].strip("'")
            if pic: pic = "images/" + pic
            c.execute("INSERT INTO yazar (id, username, print("Error:", e, "cols len:", len(cols)); breakword, name, image_path) VALUES (?, ?, ?, ?, ?)",
                      (y_id, 'yazar' + str(y_id), '123456', name, pic))
        except Exception as e:
            print("Error parsing yazar:", e)

matches = re.finditer(r'INSERT INTO `burokratlar_haberkoseyazi` \([^)]+\) VALUES (.*?);', sql_text, re.DOTALL)
for match in matches:
    values_str = match.group(1)
    records = values_str.split("),(")
    for rec in records:
        rec = rec.strip("()")
        cols = []
        in_quote = False
        current = ""
        prev_char = ""
        for char in rec:
            if char == "'" and prev_char != "\\":
                in_quote = not in_quote
            elif char == "," and not in_quote:
                cols.append(current)
                current = ""
            else:
                current += char
            prev_char = char
        cols.append(current)
        
        try:
            k_id = int(cols[0])
            head = cols[1].strip("'").replace("\\'", "'")
            info = cols[5].strip("'").replace("\\'", "'").replace("\\r\\n", "\n").replace("\\n", "\n")
            gid = int(cols[7])
            
            c.execute("INSERT INTO kose_yazisi (id, title, content, yazar_id) VALUES (?, ?, ?, ?)",
                      (k_id, head, info, gid))
        except Exception as e:
            print("Error:", e, "cols len:", len(cols)); break

conn.commit()
c.execute("SELECT COUNT(*) FROM yazar")
print("Yazar imported:", c.fetchone()[0])
c.execute("SELECT COUNT(*) FROM kose_yazisi")
print("KoseYazisi imported:", c.fetchone()[0])
conn.close()
