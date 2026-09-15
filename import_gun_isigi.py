import os
import zipfile
import xml.etree.ElementTree as ET
import sqlite3
import datetime
import re

folder = r"C:\Users\turga\OneDrive\Desktop\YÜCEL CAN GÜN IŞIĞI GAZETESİ KÖŞE YAZILARI"

def get_docx_text(path):
    try:
        document = zipfile.ZipFile(path)
        xml_content = document.read('word/document.xml')
        document.close()
        tree = ET.XML(xml_content)
        namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        paragraphs = []
        for paragraph in tree.iterfind('.//w:p', namespace):
            texts = [node.text for node in paragraph.iterfind('.//w:t', namespace) if node.text]
            if texts:
                paragraphs.append(''.join(texts))
        return '<br><br>'.join(paragraphs)
    except Exception as e:
        return str(e)

def normalize_title(t):
    # Remove dates like 12.05.2025 or 12-05-2025 and dashes
    t = re.sub(r'^\d{2}[\.\-]\d{2}[\.\-]\d{4}[\s\-]*', '', t)
    t = t.replace('.docx', '').replace('.DOCX', '').strip().lower()
    return t

conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()

yazar_id = 1

# Fetch existing titles
c.execute("SELECT title FROM kose_yazisi WHERE yazar_id = ?", (yazar_id,))
existing_titles = set(normalize_title(row[0]) for row in c.fetchall())

count = 0
skipped = 0

for filename in os.listdir(folder):
    if filename.lower().endswith(".docx") and not filename.startswith('~'):
        base_title = normalize_title(filename)
        
        if base_title in existing_titles:
            skipped += 1
            continue
            
        parts = filename.replace('.docx', '').replace('.DOCX', '').split('-', 1)
        if len(parts) == 2:
            date_str = parts[0].strip()
            title = parts[1].strip()
            try:
                dt = datetime.datetime.strptime(date_str, '%d.%m.%Y')
                date_added = dt.strftime('%Y-%m-%d 00:00:00')
            except ValueError:
                date_added = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_str = ""
            title = filename.replace('.docx', '')
            date_added = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
        full_title = f"{date_str} - {title}" if date_str else title
        full_title = full_title.strip(' -')
        
        content = get_docx_text(os.path.join(folder, filename))
        
        c.execute("INSERT INTO kose_yazisi (yazar_id, title, content, date_added) VALUES (?, ?, ?, ?)", (yazar_id, full_title, content, date_added))
        existing_titles.add(base_title)
        count += 1

conn.commit()
conn.close()
print(f"Imported {count} new articles. Skipped {skipped} duplicates.")
