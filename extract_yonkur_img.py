import os, bs4, re

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
sql = open(sql_path, encoding='utf-8', errors='ignore').read()

yonkur_html = '<h3>Yönetim Kurulu</h3><div class="row">'
for line in sql.split('\n'):
    if line.startswith('INSERT INTO `burokratlar_yonkur`'):
        # match structure: (id, 'durum', ordernum, 'grup', 'name', 'unvan', 'cv', ...
        pattern = r"\((?P<id>\d+),'(?P<durum>\d+)',(?P<ordernum>\d+),'[^']*','(?P<name>.*?)','(?P<unvan>.*?)','(?P<cv>.*?)',"
        matches = re.finditer(pattern, line)
        for m in matches:
            id_val = m.group('id')
            name = m.group('name').replace('\\\'', '\'')
            title = m.group('unvan').replace('\\\'', '\'')
            desc = m.group('cv').replace('\\\'', '\'').replace('\\r\\n', '<br>').replace('\\n', '<br>').replace('\\"', '"')
            
            image_path = f'data/yonkur/{id_val}.jpg'
            # Fallback to an empty avatar if image doesn't exist
            img_tag = f'<img src="{image_path}" style="width:150px; height:150px; object-fit:cover; border-radius:8px; border:2px solid #ddd; margin-right:20px; float:left;" onerror="this.style.display=\\\'none\\\'">'
            
            yonkur_html += f'''
            <div class="col-md-12 mb-4" style="margin-bottom:20px; border-bottom:1px solid #eee; padding-bottom:15px; clear:both;">
                {img_tag}
                <div style="overflow:hidden;">
                    <h4 style="color:#800000; margin-top:0;">{name}</h4>
                    <h5 style="color:#555; font-weight:bold;">{title}</h5>
                    <p style="font-size:13px; color:#666;">{desc}</p>
                </div>
            </div>
            '''
yonkur_html += '</div>'

filename = 'yonetimkurulu.html'
if os.path.exists(filename):
    f_html = open(filename, encoding='utf-8', errors='ignore').read()
    soup = bs4.BeautifulSoup(f_html, 'lxml')
    panels = soup.find_all('div', class_='panel-body')
    if panels:
        content_div = panels[-1]
        box = content_div.find('div', class_='box')
        new_content = bs4.BeautifulSoup(yonkur_html, 'html.parser')
        if box:
            box.clear()
            box.append(new_content)
        else:
            content_div.clear()
            content_div.append(new_content)
            
        open(filename, 'w', encoding='utf-8').write(str(soup))
        print('Updated yonetimkurulu.html with images')
        
        # also update db
        from app import app, db, Page
        with app.app_context():
            page = Page.query.filter_by(slug='yonetimkurulu').first()
            if page:
                page.content = str(box) if box else str(panels[-1])
            db.session.commit()
