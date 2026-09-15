import re
sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
sql = open(sql_path, encoding='utf-8', errors='ignore').read()
groups = set()
for line in sql.split('\n'):
    if line.startswith('INSERT INTO `burokratlar_yonkur`'):
        matches = re.finditer(r"\(\d+,'\d+',\d+,'([^']*)'", line)
        for m in matches:
            groups.add(m.group(1))
print('Yonkur groups:', groups)

import bs4
# Let's also check what bskbr.php originally did.
bskbr = open(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\homedir\public_html\module\yonkur\bskbr.php', encoding='utf-8', errors='ignore').read()
if "grup='b'" in bskbr or "grup=" in bskbr:
    print('Found grup logic in bskbr.php')
