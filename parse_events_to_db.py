import sqlite3
import bs4
import re
import os

# 1. Add location column to Etkinlik if not exists
db_path = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', 'instance', 'cms.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

try:
    c.execute("ALTER TABLE etkinlik ADD COLUMN location VARCHAR(255)")
except sqlite3.OperationalError:
    pass # Column already exists

# 2. Clear old broken events
c.execute("DELETE FROM etkinlik")

# 3. Read perfect etkinlik.html and parse events
html_path = os.path.join(r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği site yedeği\burokratlarbirligi.org', 'etkinlik.html')
with open(html_path, 'r', encoding='utf-8', errors='surrogateescape') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')
main_div = soup.find('div', id='main')

if main_div:
    panel_body = main_div.find('div', class_='panel-body')
    
    # The structure in HTML:
    # <h4><a ...> Konu : 28 ŞUBAT ... </a></h4>
    # <span>Açıklama : ... </span><br> Tarih : <b>...</b> Saat : <b>...</b> <br> Yer : ...
    # <div class="col-md-12"></div>
    
    events = []
    
    # Every h4 is a new event
    h4s = panel_body.find_all('h4')
    for h4 in h4s:
        title = ""
        if h4.a:
            title = h4.a.get_text(strip=True).replace("Konu :", "").strip()
        else:
            title = h4.get_text(strip=True).replace("Konu :", "").strip()
            
        # The next sibling span is the description
        desc_span = h4.find_next_sibling('span')
        desc = ""
        if desc_span:
            # text without the nested spans sometimes
            desc = desc_span.get_text(separator=' ', strip=True).replace("Açıklama :", "").strip()
            
        # Find Tarih and Saat and Yer in the text of panel_body between this h4 and next h4
        # Since it's unstructured text, let's just parse the full string between elements
        
    # Actually, a regex on the raw HTML is much more robust because BS4 loses text nodes between tags
    raw_html = "".join(str(item) for item in panel_body.contents)
    
    # Split by h4
    blocks = re.split(r'<h4[^>]*>', raw_html)
    for block in blocks[1:]:
        # title is inside <a ...> ... </a></h4>
        m_title = re.search(r'<a[^>]*>(?:<br\s*/?>)?\s*Konu\s*:\s*(.*?)</a>', block, re.IGNORECASE | re.DOTALL)
        if not m_title:
            # try without <a>
            m_title = re.search(r'Konu\s*:\s*(.*?)</h4>', block, re.IGNORECASE | re.DOTALL)
            
        title = m_title.group(1).strip() if m_title else "İsimsiz Etkinlik"
        
        # description is between <span>Açıklama : and </span>\s*<br/>\s*Tarih
        m_desc = re.search(r'Açıklama\s*:\s*<span[^>]*>(.*?)</span>', block, re.IGNORECASE | re.DOTALL)
        if not m_desc:
            m_desc = re.search(r'Açıklama\s*:\s*(.*?)<br', block, re.IGNORECASE | re.DOTALL)
        desc = bs4.BeautifulSoup(m_desc.group(1), 'html.parser').get_text(strip=True) if m_desc else ""
        
        # Tarih
        m_tarih = re.search(r'Tarih\s*:\s*(?:<b>)?\s*([\d\s]+)\s*(?:</b>)?', block, re.IGNORECASE | re.DOTALL)
        edate = m_tarih.group(1).strip() if m_tarih else ""
        
        # Saat
        m_saat = re.search(r'Saat\s*:\s*(?:<b>)?\s*([\d:]+)\s*(?:</b>)?', block, re.IGNORECASE | re.DOTALL)
        saat = m_saat.group(1).strip() if m_saat else ""
        
        # Yer
        m_yer = re.search(r'Yer\s*:\s*(.*?)(?:<div|$)', block, re.IGNORECASE | re.DOTALL)
        location = m_yer.group(1).strip() if m_yer else ""
        
        c.execute("INSERT INTO etkinlik (title, description, edate, saat, type, link, location) VALUES (?, ?, ?, ?, 'meeting', '', ?)", (title, desc, edate, saat, location))
        print(f"Parsed: {title}")

conn.commit()
conn.close()
print("Etkinlikler parsed and inserted into DB!")
