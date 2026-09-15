import sqlite3
import csv
from io import StringIO

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
db_path = r'instance/cms.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

with open(sql_path, 'r', encoding='utf8', errors='ignore') as f:
    text = f.read()

parts = text.split('INSERT INTO `burokratlar_haberkoseyazi`')
print("Found", len(parts) - 1, "INSERT blocks for kose_yazisi")

for part in parts[1:]:
    end_idx = part.find(';')
    if end_idx == -1: continue
    
    stmt = part[:end_idx]
    val_idx = stmt.find('VALUES')
    if val_idx == -1: continue
    
    val_str = stmt[val_idx+6:].strip()
    
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
            
    print("Extracted tuples:", len(tuples))
    if len(tuples) > 0:
        print("First tuple:", tuples[0])
        print("Length of first tuple:", len(tuples[0]))
        
        try:
            k_id = int(tuples[0][0].strip())
            print("parsed id:", k_id)
            head = tuples[0][1].strip("'")
            print("parsed head:", head)
        except Exception as e:
            print("error:", e)
    break
