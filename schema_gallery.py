import re
dump_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Extract burokratlar_gallery and burokratlar_gallerygroup definitions
import bs4
for t_name in ['burokratlar_gallerygroup', 'burokratlar_gallery']:
    m = re.search(f"CREATE TABLE `{t_name}` \\((.*?)\\) ENGINE=", text, re.DOTALL)
    if m:
        print(f"--- {t_name} Schema ---")
        print(m.group(1).strip())
        
    print(f"--- {t_name} Data Sample ---")
    data_match = re.search(f"INSERT INTO `{t_name}` VALUES (.*?);", text, re.DOTALL)
    if data_match:
        print(data_match.group(1)[:1000])
