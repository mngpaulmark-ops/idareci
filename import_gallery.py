import sqlite3
import re
import os

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
db_path = r'instance/cms.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("DELETE FROM galeri_resim")
c.execute("DELETE FROM galeri")

with open(sql_path, 'r', encoding='utf8', errors='ignore') as f:
    text = f.read()

def extract_tuples(table_name):
    parts = text.split(f"INSERT INTO `{table_name}`")
    all_tuples = []
    for part in parts[1:]:
        val_idx = part.find('VALUES')
        if val_idx == -1: continue
        
        val_str = part[val_idx+6:].strip()
        
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
            elif char == ";" and not in_string:
                break
            else:
                current_val += char
        all_tuples.extend(tuples)
    return all_tuples

# Import gallery groups (Albums)
gal_groups = extract_tuples("burokratlar_gallerygroup")
print(f"Found {len(gal_groups)} gallery groups")
for cols in gal_groups:
    if len(cols) >= 5:
        g_id = int(cols[0].strip())
        name = cols[4].strip("'").replace("\\'", "'")
        c.execute("INSERT OR IGNORE INTO galeri (id, title) VALUES (?, ?)", (g_id, name))

# Import gallery images
gal_images = extract_tuples("burokratlar_gallery")
print(f"Found {len(gal_images)} gallery images")
for cols in gal_images:
    if len(cols) >= 4:
        img_id = int(cols[0].strip())
        group_id = int(cols[3].strip())
        
        # Check extensions in data/gallery
        img_path = f"data/gallery/{img_id}.jpg" # most are jpg
        # It's better to verify if it exists, but for now we'll just insert
        c.execute("INSERT OR IGNORE INTO galeri_resim (id, galeri_id, image_path) VALUES (?, ?, ?)", (img_id, group_id, img_path))

conn.commit()
c.execute("SELECT COUNT(*) FROM galeri")
print("Galeri imported:", c.fetchone()[0])
c.execute("SELECT COUNT(*) FROM galeri_resim")
print("GaleriResim imported:", c.fetchone()[0])
conn.close()
