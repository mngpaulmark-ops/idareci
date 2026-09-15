import sqlite3
import re

sql_file = r"C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql"

insert_stmt = "INSERT INTO `burokratlar_etkinlik` VALUES "

records = []
with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if line.startswith(insert_stmt):
            values_str = line[len(insert_stmt):].strip().rstrip(';')
            # Quick split by '),(' to get rows
            rows = values_str.split('),(')
            for r in rows:
                r = r.strip('()')
                # basic split by comma, naive but maybe enough if no commas in text, but wait, text HAS commas!
                pass

# Let's use regex instead
import re
with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

match = re.search(r"INSERT INTO `burokratlar_etkinlik` VALUES (.*?);", content, re.DOTALL)
if match:
    # use ast.literal_eval trick or regex
    # format is (id, cat_id, title, description, link, date, time)
    val_str = match.group(1)
    # Split by '),'
    row_strs = val_str.split('),(')
    
    conn = sqlite3.connect('cms.db')
    c = conn.cursor()
    # Ensure table exists
    c.execute("CREATE TABLE IF NOT EXISTS etkinlik (id INTEGER PRIMARY KEY, title VARCHAR(200), description TEXT, edate VARCHAR(20), saat VARCHAR(10), link VARCHAR(255), type VARCHAR(50))")
    
    count = 0
    for r in row_strs:
        r = r.strip('()')
        # Splitting correctly with regex
        cols = re.findall(r"(?:'((?:[^']|\\')*)'|(\d+|NULL))", r)
        # cols is a list of tuples like [("1", ""), ("", "0"), ("Title", ""), ...]
        clean_cols = [c[0] if c[0] else c[1] for c in cols]
        if len(clean_cols) >= 5:
            # Table schema in PHP: id, group, date, time, title, detail
            # Let's assume order: id, group_id, date, time, title, detail
            # Let's print the cols to see what it looks like
            c.execute("INSERT OR REPLACE INTO etkinlik (id, edate, saat, title, description) VALUES (?, ?, ?, ?, ?)", 
                      (clean_cols[0], clean_cols[2], clean_cols[3], clean_cols[4].replace("\\'", "'"), clean_cols[5].replace("\\'", "'")))
            count += 1
    
    conn.commit()
    conn.close()
    print(f"Imported {count} events into cms.db")
else:
    print("No INSERT found for etkinlik")
