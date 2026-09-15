import sqlite3
import csv
from io import StringIO

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'

with open(sql_path, 'r', encoding='utf8', errors='ignore') as f:
    text = f.read()

parts = text.split('INSERT INTO `burokratlar_haberkoseyazi`')
for part in parts[1:]:
    print("-----")
    print(part[:300])
