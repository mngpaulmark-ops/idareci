import os
path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if 'INSERT INTO `burokratlar_yonkur`' in line:
            parts = line.split('),(')
            groups = set()
            for p in parts:
                cols = p.split(',')
                if len(cols) > 4:
                    groups.add(cols[3].strip("'"))
            print('Yonkur groups:', groups)
            
        if 'INSERT INTO `burokratlar_page`' in line:
            parts = line.split('),(')
            for p in parts:
                if 'temsil' in p.lower():
                    print('Found Temsil in Page:', p[:200])
