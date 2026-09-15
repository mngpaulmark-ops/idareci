import os, bs4, re
from collections import defaultdict

sql_path = r'C:\Users\turga\OneDrive\Desktop\bürokratlar birliği orjinal site yedeği\backup-8.11.2026_11-19-03_burokratlarbirli\backup-8.11.2026_11-19-03_burokratlarbirli\mysql\burokratlarbirli_database.sql'
sql = open(sql_path, encoding='utf-8', errors='ignore').read()

groups = defaultdict(list)

for line in sql.split('\n'):
    if line.startswith('INSERT INTO `burokratlar_yonkur`'):
        pattern = r"\((?P<id>\d+),'(?P<durum>\d+)',(?P<ordernum>\d+),'(?P<grup>[^']*)','(?P<name>.*?)','(?P<unvan>.*?)','(?P<cv>.*?)',"
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

# Sort by ordernum
for g in groups:
    groups[g] = sorted(groups[g], key=lambda x: x['ordernum'])

def generate_group_html(title, members):
    if not members:
        return ''
    html = f'''
    <div class="panel-body">
        <center><h3 class="heading-1"><span>{title}</span></h3></center>
        <div class="row justify-content-center center" style="display:flex; flex-wrap:wrap; justify-content:center;">
    '''
    for member in members:
        id_val = member['id']
        name = member['name']
        unvan = member['unvan']
        image_path = f'data/yonkur/{id_val}.jpg'
        
        # We need a fallback if the image doesn't exist
        img_tag = f'<img class="rounded-circle mx-auto d-inline-block shadow-sm" src="{image_path}" alt="{name}" style="width:120px; height:120px; object-fit:cover; border:5px solid #fff; border-radius:50%; box-shadow:0 4px 8px rgba(0,0,0,0.1);" onerror="this.src=\\\'images/default-avatar.png\\\'; this.onerror=null;">'
        
        html += f'''
        <div class="col-12 col-md-6 col-lg-4" style="margin-bottom:60px;">
            <div class="card border-0 shadow-lg position-relative" style="background:#fff; border-radius:10px; box-shadow:0 10px 20px rgba(0,0,0,0.08); margin-top:50px;">
                <div class="card-body p-4">
                    <div class="member-profile position-absolute w-100 text-center" style="top:-60px; left:0; right:0;"> 
                        {img_tag}
                    </div>
                    <div class="card-text text-center" style="padding-top:60px;">
                        <h5 class="member-name mb-1 text-primary font-weight-bold" style="color:#800000; font-size:16px; margin-bottom:5px;">{name}</h5>
                        <div class="mb-3 text-center" style="font-size:14px; color:#666; min-height:40px;">{unvan}</div>
                    </div>
                </div>
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
        # Just replace the last panel body entirely or the box
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
        print('Updated yonetimkurulu.html with correct original CSS structure')
        
        # update DB for admin panel sync
        from app import app, db, Page
        with app.app_context():
            page = Page.query.filter_by(slug='yonetimkurulu').first()
            if page:
                page.content = str(box) if box else str(panels[-1])
            db.session.commit()
