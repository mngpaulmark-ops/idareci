import sqlite3
import re
import bs4
from datetime import datetime

def update_homepage_slider():
    conn = sqlite3.connect('instance/cms.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get all authors
    c.execute("SELECT * FROM yazar")
    yazarlar = c.fetchall()
    
    author_latest = []
    
    for yazar in yazarlar:
        yazar_id = yazar['id']
        name = yazar['name']
        pic = yazar['image_path'] if yazar['image_path'] else 'themes/burokratlar/tema/images/no-image.png'
        
        # Get all articles for this author
        c.execute("SELECT * FROM kose_yazisi WHERE yazar_id = ?", (yazar_id,))
        yazilar = c.fetchall()
        
        if not yazilar:
            continue
            
        articles = []
        for yazi in yazilar:
            title = yazi['title']
            
            # extract date
            m = re.search(r'(\d{1,2})[\.\-](\d{1,2})[\.\-](\d{4})', title)
            dt = datetime(1900, 1, 1)
            if m:
                try:
                    dt = datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
                except:
                    pass
            
            # fix typo dates if they are in DB but we fixed them in HTML
            # wait, the html was already fixed, but let's make sure our sorting handles the corrected strings
            # well, our regex handles it or we can just replace string here
            fixed_title = title.replace('24.11.20220', '24.11.2022').replace('23.02.20222', '23.02.2022')
            
            m = re.search(r'(\d{1,2})[\.\-](\d{1,2})[\.\-](\d{4})', fixed_title)
            if m:
                try:
                    dt = datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
                except:
                    pass
                    
            articles.append((dt, yazi['id'], fixed_title))
            
        # Sort articles for this author
        articles.sort(key=lambda x: (x[0], x[1]), reverse=True)
        latest_article = articles[0]
        
        author_latest.append({
            'author_name': name,
            'author_pic': pic,
            'latest_dt': latest_article[0],
            'latest_id': latest_article[1],
            'latest_title': latest_article[2]
        })
        
    # Sort authors by the date of their latest article
    author_latest.sort(key=lambda x: (x['latest_dt'], x['latest_id']), reverse=True)
    
    # Generate the <ul> html
    ul_content = "<ul>\n"
    for item in author_latest:
        short_title = item['latest_title']
        # remove the date part for the short title if you want, but old code kept it or shortened it.
        # let's just strip html and truncate
        short_title = short_title[:50] + "..." if len(short_title) > 50 else short_title
        
        # NOTE: Using kose-yazilari-{id}.html because that's what our generator makes!
        ul_content += f'''
        <li class="kayan"><a href="kose-yazilari-{item["latest_id"]}.html">
        <img alt="{item["author_name"]}" class="yazar" src="{item["author_pic"]}" style=" border-radius: 10px;"/>
        <p><b>{item["author_name"]}</b></p></a>
        <span>{short_title}</span>
        <div class="clearfix"></div></li>
        '''
    ul_content += "</ul>"
    
    # Update anasayfa.html
    with open('anasayfa.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = bs4.BeautifulSoup(html, 'html.parser')
    kayan_alan = soup.find('div', id='kayan_alan')
    if kayan_alan:
        old_ul = kayan_alan.find('ul')
        if old_ul:
            old_ul.replace_with(bs4.BeautifulSoup(ul_content, 'html.parser'))
            
            with open('anasayfa.html', 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print("Updated anasayfa.html successfully!")
        else:
            print("Could not find ul inside kayan_alan.")
    else:
        print("Could not find div#kayan_alan in anasayfa.html.")
        
update_homepage_slider()
