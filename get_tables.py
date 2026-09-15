import re
sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
sql = open(sql_path, encoding='utf-8', errors='ignore').read()
tables = set()
for line in sql.split('\n'):
    if line.startswith('CREATE TABLE'):
        m = re.search(r'CREATE TABLE `([^`]+)`', line)
        if m: tables.add(m.group(1))
for t in sorted(tables):
    print(t)
