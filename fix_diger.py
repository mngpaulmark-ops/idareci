import sqlite3
import os
import bs4

db_path = os.path.join('instance', 'cms.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('SELECT id, content_html FROM page WHERE slug="diger-kurullar"')
res = c.fetchone()

if res:
    page_id = res[0]
    content_html = res[1]
    
    # We want to center everything.
    soup = bs4.BeautifulSoup(content_html, 'html.parser')
    for p in soup.find_all('p'):
        p['style'] = 'text-align: center;'
    
    for img in soup.find_all('img'):
        style = img.get('style', '')
        if 'margin: 0 auto' not in style:
            img['style'] = style + '; margin: 0 auto; display: inline-block;'
            
    new_content_html = str(soup)
    c.execute('UPDATE page SET content_html = ? WHERE id = ?', (new_content_html, page_id))
    conn.commit()
    print('DB updated for diger-kurullar')

conn.close()
