import sqlite3
import re
import bs4
from datetime import datetime

def update_kose_yazarlari_page():
    conn = sqlite3.connect('instance/cms.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM yazar")
    yazarlar = c.fetchall()
    
    author_latest = []
    
    for yazar in yazarlar:
        yazar_id = yazar['id']
        name = yazar['name']
        pic = yazar['image_path'] if yazar['image_path'] else 'themes/burokratlar/tema/images/no-image.png'
        
        c.execute("SELECT * FROM kose_yazisi WHERE yazar_id = ?", (yazar_id,))
        yazilar = c.fetchall()
        
        if not yazilar:
            continue
            
        articles = []
        for yazi in yazilar:
            title = yazi['title']
            fixed_title = title.replace('24.11.20220', '24.11.2022').replace('23.02.20222', '23.02.2022')
            
            m = re.search(r'(\d{1,2})[\.\-](\d{1,2})[\.\-](\d{4})', fixed_title)
            dt = datetime(1900, 1, 1)
            if m:
                try:
                    dt = datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
                except:
                    pass
            articles.append((dt, yazi['id'], fixed_title))
            
        articles.sort(key=lambda x: (x[0], x[1]), reverse=True)
        latest_article = articles[0]
        
        author_latest.append({
            'yazar_id': yazar_id,
            'author_name': name,
            'author_pic': pic,
            'latest_dt': latest_article[0],
            'latest_id': latest_article[1]
        })
        
    author_latest.sort(key=lambda x: (x['latest_dt'], x['latest_id']), reverse=True)
    
    html = ''
    for item in author_latest:
        html += f'''
        <div class="col-md-4" style="text-align: center; margin-bottom: 20px;">
            <a href="kose-yazar-{item["yazar_id"]}.html">
                <img src="{item["author_pic"]}" style="max-width: 150px; border-radius: 50%; height: 150px; object-fit: cover;"/>
                <br/><b>{item["author_name"]}</b>
            </a>
        </div>
        '''
        
    with open('kose-yazarlari.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    soup = bs4.BeautifulSoup(content, 'html.parser')
    panel_body = soup.find('div', class_='panel-heading', string=re.compile(r'K.*Yazarlar')).find_next_sibling('div', class_='panel-body')
    
    if panel_body:
        panel_body.clear()
        panel_body.append(bs4.BeautifulSoup(html, 'html.parser'))
        
        with open('kose-yazarlari.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print("Updated kose-yazarlari.html!")
    else:
        print("Could not find panel body.")

update_kose_yazarlari_page()
