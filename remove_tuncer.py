import os
import re
import sqlite3

# 1. Clean HTML files
for root, d, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or 'venv' in root: continue
    for f in files:
        if f.endswith(('.html', '.py', '.txt')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                
                # Replace meta tags
                new_content = re.sub(r'<meta[^>]*tuncer[^>]*>\n?', '', content, flags=re.IGNORECASE)
                
                # Replace literal text "Yazar", "Yazar"
                new_content = re.sub(r'tuncer\s+ünal', 'Yazar', new_content, flags=re.IGNORECASE)
                new_content = re.sub(r'tuncer\s+unal', 'Yazar', new_content, flags=re.IGNORECASE)
                
                if content != new_content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f"Cleaned {path}")
            except Exception as e:
                pass

# 2. Clean Database (Delete Yazar from Yazar if exists)
try:
    conn = sqlite3.connect('cms.db')
    c = conn.cursor()
    # Find Yazar
    c.execute("SELECT id FROM yazar WHERE name LIKE '%Tuncer%'")
    rows = c.fetchall()
    for row in rows:
        yid = row[0]
        c.execute("DELETE FROM yazar WHERE id = ?", (yid,))
        c.execute("DELETE FROM kose_yazisi WHERE yazar_id = ?", (yid,))
        print(f"Deleted Yazar {yid} and their articles")
    conn.commit()
    conn.close()
except Exception as e:
    pass

# We also check if there are html files under `koseyazisi` for this author and delete them?
# The static HTML files might exist in koseyazisi/ folder.
# We can search for the term "tuncer" in paths and delete those files or directories.
