import os, bs4, re

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
sql = open(sql_path, encoding='utf-8', errors='ignore').read()

yonkur_html = '<h3>Yönetim Kurulu</h3><div class="row">'
for line in sql.split('\n'):
    if line.startswith('INSERT INTO `burokratlar_yonkur`'):
        # Parse the tuples
        # VALUES (1,'1',1,'ya','Yücel CAN','Yönetim Kurulu Başkanı','<strong>ULUS...','','',...
        # Let's just use regex to extract (id, '1', 1, 'ya', 'Name', 'Title', 'Description')
        pattern = r"\(\d+,'\d+',\d+,'[^']*','(.*?)','(.*?)','(.*?)',"
        matches = re.finditer(pattern, line)
        for m in matches:
            name = m.group(1).replace('\\\'', '\'')
            title = m.group(2).replace('\\\'', '\'')
            desc = m.group(3).replace('\\\'', '\'').replace('\\r\\n', '<br>').replace('\\n', '<br>').replace('\\"', '"')
            
            yonkur_html += f'''
            <div class="col-md-12 mb-4" style="margin-bottom:20px; border-bottom:1px solid #ccc; padding-bottom:15px;">
                <h4 style="color:#800000;">{name}</h4>
                <h5 style="color:#555;">{title}</h5>
                <p>{desc}</p>
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
            
        headings = soup.find_all('div', class_='panel-heading')
        if headings:
            headings[-1].string = 'İdareci ve Bürokratlar Birliği / Yönetim Kurulu'
            
        open(filename, 'w', encoding='utf-8').write(str(soup))
        print('Updated yonetimkurulu.html')
