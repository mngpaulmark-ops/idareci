import re
dump_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

tables = re.findall(r'CREATE TABLE `([^`]+)`', text)
for t in tables:
    if 'galeri' in t.lower() or 'foto' in t.lower() or 'album' in t.lower() or 'resim' in t.lower():
        print(t)
