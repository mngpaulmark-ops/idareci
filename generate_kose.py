import os
import bs4
import sqlite3

def regenerate_all_kose():
    conn = sqlite3.connect('instance/cms.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # 1. Yazar profiles (kose-yazar-<id>.html)
    c.execute("SELECT * FROM yazar")
    yazarlar = c.fetchall()
    
    # Base template: we can use hakkimizda.html
    if not os.path.exists('hakkimizda.html'):
        return
        
    with open('hakkimizda.html', 'r', encoding='utf-8', errors='ignore') as f:
        base_html = f.read()
    
    for yazar in yazarlar:
        soup = bs4.BeautifulSoup(base_html, 'lxml')
        main_div = soup.find('div', class_='col-md-9')
        if not main_div: continue
        
        # Build author content
        yazar_id = yazar['id']
        name = yazar['name']
        pic = yazar['image_path'] if yazar['image_path'] else 'themes/burokratlar/tema/images/no-image.png'
        
        c.execute("SELECT * FROM kose_yazisi WHERE yazar_id = ? ORDER BY date_added DESC, id DESC", (yazar_id,))
        yazilar = c.fetchall()
        
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
                                {''.join([f'<li><a href="kose-yazilari-{y["id"]}.html">{y["title"]}</a></li>' for y in yazilar])}
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
            
    # 2. Articles (kose-yazilari-<id>.html)
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
    print("Generated all Yazar and KoseYazisi HTML files.")

if __name__ == '__main__':
    regenerate_all_kose()
