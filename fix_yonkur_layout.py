import os, bs4, re
from collections import defaultdict

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
sql = open(sql_path, encoding='utf-8', errors='ignore').read()

groups = defaultdict(list)
for line in sql.split('\n'):
    if line.startswith('INSERT INTO `burokratlar_yonkur`'):
        pattern = r"\((?P<id>\d+),'(?P<durum>\d+)',(?P<ordernum>\d+),'(?P<grup>[^']*)','(?P<name>.*?)','(?P<unvan>.*?)',"
        matches = re.finditer(pattern, line)
        for m in matches:
            member = {
                'id': m.group('id'),
                'durum': m.group('durum'),
                'ordernum': int(m.group('ordernum')),
                'grup': m.group('grup'),
                'name': m.group('name').replace('\\\'', '\''),
                'unvan': m.group('unvan').replace('\\\'', '\''),
            }
            if member['durum'] == '1':
                groups[member['grup']].append(member)

for g in groups:
    groups[g] = sorted(groups[g], key=lambda x: x['ordernum'])

def generate_group_html(title, members):
    if not members:
        return ''
    html = f'''
    <div class="panel-body">
        <center><h3 class="heading-1" style="margin-bottom:30px; margin-top:20px;"><span>{title}</span></h3></center>
        <div class="row justify-content-center" style="display:flex; flex-wrap:wrap; justify-content:center; gap: 20px;">
    '''
    for member in members:
        id_val = member['id']
        name = member['name']
        unvan = member['unvan']
        image_path = f'data/yonkur/{id_val}.jpg'
        
        html += f'''
        <div class="col-12 col-md-4 col-lg-3" style="margin-bottom:30px; display:flex;">
            <div class="card border-0 shadow" style="background:#fff; border-radius:15px; padding:25px 15px; text-align:center; box-shadow:0 8px 20px rgba(0,0,0,0.08); width:100%; border: 1px solid #f1f1f1;">
                <img src="{image_path}" style="width:130px; height:130px; border-radius:50%; object-fit:cover; margin:0 auto 20px auto; border:4px solid #eaeaea; box-shadow:0 4px 10px rgba(0,0,0,0.1);" onerror="this.src='images/default-avatar.png'; this.onerror=null;">
                <h5 style="color:#800000; font-size:17px; font-weight:700; margin-bottom:8px; line-height:1.3;">{name}</h5>
                <div style="font-size:13px; color:#666; font-weight:500; min-height:40px;">{unvan}</div>
            </div>
        </div>
        '''
    html += '</div></div><div class="clearfix"></div>'
    return html

yonkur_html = '<div class="main"><div class="panel panel-primary"><div class="panel-heading" style="display:none;">Yönetim Kurulu Listesi</div>'
yonkur_html += generate_group_html('Yönetim Kurulu Üyelerimiz', groups['ya'])
yonkur_html += generate_group_html('Yönetim Kurulu Yedek Üyelerimiz', groups['yy'])
yonkur_html += generate_group_html('Denetleme Kurulu Üyelerimiz', groups['da'])
yonkur_html += generate_group_html('Denetleme Kurulu Yedek Üyelerimiz', groups['dy'])
yonkur_html += '</div></div>'

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
        
        from app import app, db, Page
        with app.app_context():
            page = Page.query.filter_by(slug='yonetimkurulu').first()
            if page:
                page.content = str(box) if box else str(panels[-1])
            db.session.commit()
