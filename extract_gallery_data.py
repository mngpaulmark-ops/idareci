import re
dump_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()
import bs4

# Find where they are inserted
for t_name in ['burokratlar_gallerygroup', 'burokratlar_gallery']:
    print(f"--- {t_name} ---")
    lines = [line for line in text.split('\n') if f"INSERT INTO `{t_name}`" in line]
    for line in lines:
        print(line[:1000])
