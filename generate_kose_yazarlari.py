import sqlite3
import bs4

def regenerate_kose_yazarlari():
    conn = sqlite3.connect('instance/cms.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM yazar")
    yazarlar = c.fetchall()
    
    with open('hakkimizda.html', 'r', encoding='utf-8', errors='ignore') as f:
        base_html = f.read()
        
    soup = bs4.BeautifulSoup(base_html, 'lxml')
    main_div = soup.find('div', class_='col-md-9')
    
    html = '''
    <div class="col-md-9" id="main">
        <div class="main">
            <div class="panel panel-primary">
                <div class="panel-heading">Köşe Yazarları</div>
                <div class="panel-body">
    '''
    
    for y in yazarlar:
        pic = y['image_path'] if y['image_path'] else 'themes/burokratlar/tema/images/no-image.png'
        html += f'''
                    <div class="col-md-4" style="text-align: center; margin-bottom: 20px;">
                        <a href="kose-yazar-{y["id"]}.html">
                            <img src="{pic}" style="max-width: 150px; border-radius: 50%; height: 150px; object-fit: cover;"/>
                            <br/><b>{y["name"]}</b>
                        </a>
                    </div>
        '''
        
    html += '''
                </div>
            </div>
        </div>
    </div>
    '''
    
    new_content = bs4.BeautifulSoup(html, 'html.parser')
    main_div.replace_with(new_content)
    
    with open('kose-yazarlari.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    conn.close()

if __name__ == '__main__':
    regenerate_kose_yazarlari()
