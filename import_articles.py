import os
import zipfile
import xml.etree.ElementTree as ET
import sqlite3
import datetime

folder = r"C:\Users\turga\OneDrive\Desktop\YÜCEL CAN HABERİN SAATİ KÖŞE YAZILARI"

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

conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()

# Get Yücel CAN yazar_id. In the DB it might have weird chars. So just use ID 1.
yazar_id = 1

count = 0
for filename in os.listdir(folder):
    if filename.lower().endswith(".docx") and not filename.startswith('~'):
        parts = filename.replace('.docx', '').replace('.DOCX', '').split('-', 1)
        if len(parts) == 2:
            date_str = parts[0].strip()
            title = parts[1].strip()
            
            # Parse date if possible
            try:
                dt = datetime.datetime.strptime(date_str, '%d.%m.%Y')
                date_added = dt.strftime('%Y-%m-%d 00:00:00')
            except ValueError:
                date_added = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_str = ""
            title = filename.replace('.docx', '')
            date_added = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
        # The user wants filename's date and title. So let's include both in the title to be safe.
        full_title = f"{date_str} - {title}" if date_str else title
        
        # Remove any leading dashes if present
        full_title = full_title.strip(' -')
        
        content = get_docx_text(os.path.join(folder, filename))
        
        c.execute("INSERT INTO kose_yazisi (yazar_id, title, content, date_added) VALUES (?, ?, ?, ?)", (yazar_id, full_title, content, date_added))
        count += 1

conn.commit()
conn.close()
print(f"Imported {count} articles.")
