import os
import bs4
import sqlite3
import re
from datetime import datetime

def extract_date(title):
    match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', title)
    if match:
        day, month, year = match.groups()
        return datetime(int(year), int(month), int(day))
    return datetime.min

def regenerate_all_kose():
    conn = sqlite3.connect('instance/cms.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Base template
    if not os.path.exists('hakkimizda.html'):
        return
        
    with open('hakkimizda.html', 'r', encoding='utf-8', errors='ignore') as f:
        base_html = f.read()
    
    # 1. Yazar profiles
    c.execute("SELECT * FROM yazar")
    yazarlar = c.fetchall()
    
    for yazar in yazarlar:
        soup = bs4.BeautifulSoup(base_html, 'lxml')
        main_div = soup.find('div', class_='col-md-9')
        if not main_div: continue
        
        yazar_id = yazar['id']
        name = yazar['name']
        pic = yazar['image_path'] if yazar['image_path'] else 'themes/burokratlar/tema/images/no-image.png'
        
        c.execute("SELECT * FROM kose_yazisi WHERE yazar_id = ?", (yazar_id,))
        yazilar = c.fetchall()
        
        # Sort chronologically by parsing title
        yazilar_sorted = sorted(yazilar, key=lambda y: extract_date(y['title']), reverse=True)
        
        new_content = bs4.BeautifulSoup(f'''
        <div class="col-md-9" id="main">
            <div class="main">
                <div class="panel panel-primary">
                    <div class="panel-heading">Görüş & Politika Notları / {name}</div>
                    <div class="panel-body">
                        <div class="col-md-4">
                            <img src="{pic}" style="float: left; max-width: 100%; margin-bottom:10px; margin-right:10px;"/>
                            <br/>
                            <h4><b>{name}</b></h4>
                        </div>
                        <div class="col-md-8">
                            <br/>
                            <h4>Yazarın Yazıları:</h4>
                            <ul>
                                {''.join([f'<li><a href="kose-yazilari-{y["id"]}.html">{y["title"]}</a></li>' for y in yazilar_sorted])}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        ''', 'html.parser')
        
        main_div.replace_with(new_content)
        
        with open(f'kose-yazar-{yazar_id}.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    # 2. Articles
    c.execute("SELECT * FROM kose_yazisi")
    yazilar = c.fetchall()
    
    for yazi in yazilar:
        soup = bs4.BeautifulSoup(base_html, 'lxml')
        main_div = soup.find('div', class_='col-md-9')
        if not main_div: continue
        
        k_id = yazi['id']
        title = yazi['title']
        content = yazi['content']
        yazar_id = yazi['yazar_id']
        
        # Get Yazar info
        c.execute("SELECT * FROM yazar WHERE id = ?", (yazar_id,))
        yazar = c.fetchone()
        
        yazar_name = yazar['name'] if yazar else "Bilinmeyen Yazar"
        yazar_pic = yazar['image_path'] if yazar and yazar['image_path'] else 'themes/burokratlar/tema/images/no-image.png'
        
        # Get all articles by this author for the dropdown/list at bottom
        c.execute("SELECT * FROM kose_yazisi WHERE yazar_id = ?", (yazar_id,))
        other_articles = c.fetchall()
        other_sorted = sorted(other_articles, key=lambda y: extract_date(y['title']), reverse=True)
        
        # We will build a select dropdown similar to what they had, but WORKING
        options = []
        for o in other_sorted:
            selected = 'selected' if o['id'] == k_id else ''
            options.append(f'<option value="kose-yazilari-{o["id"]}.html" {selected}>{o["title"]}</option>')
        
        dropdown_html = f'''
        <div style="margin-top: 30px; padding: 15px; background: #f9f9f9; border: 1px solid #ddd; border-radius: 4px;">
            <h4>Yazara Ait Diğer Yazılar</h4>
            <p>Yazarın diğer yazılarını okumak için aşağıdan seçiniz veya <a href="kose-yazar-{yazar_id}.html">tüm yazılarına göz atın</a>.</p>
            <select class="form-control" onchange="if (this.value) window.location.href=this.value;" style="font-size:16px; height:45px;">
                {''.join(options)}
            </select>
        </div>
        '''
        
        new_content = bs4.BeautifulSoup(f'''
        <div class="col-md-9" id="main">
            <div class="main">
                <div class="panel panel-primary">
                    <div class="panel-heading">Görüş & Politika Notları / {title}</div>
                    <div class="panel-body">
                        <div class="col-md-12">
                            <div style="float: left; margin-right: 15px; margin-bottom: 15px; text-align: center;">
                                <a href="kose-yazar-{yazar_id}.html">
                                    <img src="{yazar_pic}" style="max-width: 150px;"/>
                                    <br/><b>{yazar_name}</b>
                                </a>
                            </div>
                            <h3>{title}</h3>
                            <hr/>
                            {'''<img src="themes/burokratlar/tema/images/yucel_can_banner.jpg" style="width:100%; max-width:100%; border-radius:8px; margin-bottom:20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"/><br/>''' if str(yazar_id) == '1' else ''}
                            <div class="content-text">
                                {content}
                            </div>
                            
                            <div class="clearfix"></div>
                            
                            <!-- ALT KISIM DİĞER YAZILAR -->
                            {dropdown_html}
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
        ''', 'html.parser')
        
        main_div.replace_with(new_content)
        
        with open(f'kose-yazilari-{k_id}.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    conn.close()
    print("Generated all Yazar and KoseYazisi HTML files with bottom list.")

if __name__ == '__main__':
    regenerate_all_kose()
