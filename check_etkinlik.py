import re
dump_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()
inserts = set(re.findall(r'INSERT INTO `([^`]+)`', text))
for i in sorted(list(inserts)):
    if 'etkinlik' in i:
        print(i)
        idx = text.find(f'INSERT INTO `{i}`')
        print(text[idx:idx+500])
