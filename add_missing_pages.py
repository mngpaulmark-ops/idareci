import sqlite3
import bs4
import os

conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()

missing_pages = [
    ('Gençlik Kolları', 'genclik-kollari'),
    ('Duyurular', 'duyurular'),
    ('Etkinlikler', 'etkinlik'),
    ('Raporlar / Belgeler', 'raporlar-belgeler')
]

for title, slug in missing_pages:
    # Check if exists
    c.execute('SELECT id FROM page WHERE slug=?', (slug,))
    if not c.fetchone():
        filename = f"{slug}.html"
        content = ""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8', errors='surrogateescape') as f:
                html = f.read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            main_div = soup.find('div', id='main')
            if main_div:
                panel_body = main_div.find('div', class_='panel-body')
                if panel_body:
                    box = panel_body.find('div', class_='box')
                    if box:
                        content = "".join(str(item) for item in box.contents).strip()
                    else:
                        content = "".join(str(item) for item in panel_body.contents).strip()
        
        c.execute('INSERT INTO page (title, slug, content_html) VALUES (?, ?, ?)', (title, slug, content))
        print(f"Added missing page: {title}")

conn.commit()
conn.close()
