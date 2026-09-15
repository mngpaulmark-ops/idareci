import sqlite3
import re
import csv
from io import StringIO

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
db_path = r'instance/cms.db'

with open(sql_path, 'r', encoding='utf8', errors='ignore') as f:
    sql_text = f.read()

conn = sqlite3.connect(db_path)
c = conn.cursor()

# c.execute("DELETE FROM kose_yazisi")

def parse_mysql_values(values_str):
    # This replaces MySQL \', \", \n, \r with their actual equivalents so python csv can parse it
    # But csv reader expects proper quotes
    return []

# Better approach: Just find all individual records using regex
# A record starts with ( and ends with ) and contains values.
# Actually we can just do a very simple split by "),(" since no article contains exactly that sequence!
count = 0
matches = re.finditer(r'INSERT INTO `burokratlar_haberkoseyazi` \([^)]+\) VALUES (.*?);', sql_text, re.DOTALL)
for match in matches:
    val_str = match.group(1).strip()
    if val_str.startswith('('): val_str = val_str[1:]
    if val_str.endswith(')'): val_str = val_str[:-1]
    
    # split by "),("
    records = val_str.split('),(')
    for rec in records:
        # Use csv reader to parse the comma separated values
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
            print("Error:", e)

conn.commit()
c.execute("SELECT COUNT(*) FROM kose_yazisi")
print("KoseYazisi imported:", c.fetchone()[0])
conn.close()
