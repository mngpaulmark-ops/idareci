import re, os, bs4

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

new_func = '''def regenerate_yonkur_html():
    from collections import defaultdict
    import bs4, os
    groups = defaultdict(list)
    members = Yonkur.query.order_by(Yonkur.ordernum).all()
    for m in members:
        groups[m.grup].append({
            'name': m.name,
            'unvan': m.unvan,
            'image_path': m.image_path if m.image_path else 'images/default-avatar.png'
        })

    def generate_group_html(title, members_list):
        if not members_list: return ''
        html = f'<div class="panel-body"><center><h3 class="heading-1" style="margin-bottom:30px; margin-top:20px;"><span>{title}</span></h3></center><div class="row justify-content-center" style="display:flex; flex-wrap:wrap; justify-content:center; gap: 20px;">'
        for member in members_list:
            html += f"""
            <div class="col-12 col-md-4 col-lg-3" style="margin-bottom:30px; display:flex;">
                <div class="card border-0 shadow" style="background:#fff; border-radius:15px; padding:25px 15px; text-align:center; box-shadow:0 8px 20px rgba(0,0,0,0.08); width:100%; border: 1px solid #f1f1f1;">
                    <img src="/{member['image_path']}" style="width:130px; height:130px; border-radius:50%; object-fit:cover; margin:0 auto 20px auto; border:4px solid #eaeaea; box-shadow:0 4px 10px rgba(0,0,0,0.1);" onerror="this.src='/images/default-avatar.png'; this.onerror=null;">
                    <h5 style="color:#800000; font-size:17px; font-weight:700; margin-bottom:8px; line-height:1.3;">{member['name']}</h5>
                    <div style="font-size:13px; color:#666; font-weight:500; min-height:40px;">{member['unvan']}</div>
                </div>
            </div>
            """
        html += '</div></div><div class="clearfix"></div>'
        return html

    def write_to_file_and_db(filename, html_content, title):
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                soup = bs4.BeautifulSoup(f.read(), 'lxml')
            panels = soup.find_all('div', class_='panel-body')
            if panels:
                content_div = panels[-1]
                box = content_div.find('div', class_='box')
                new_content = bs4.BeautifulSoup(html_content, 'html.parser')
                if box:
                    box.clear()
                    box.append(new_content)
                else:
                    content_div.clear()
                    content_div.append(new_content)
                
                # Update title
                headings = soup.find_all('div', class_='panel-heading')
                if headings:
                    headings[-1].string = f'İdareci ve Bürokratlar Birliği / {title}'

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                
                slug = filename.replace('.html', '')
                page = Page.query.filter_by(slug=slug).first()
                if page:
                    page.content = str(box) if box else str(panels[-1])
                db.session.commit()
        else:
            print(f"Warning: {filename} does not exist. Using hakkimizda as template.")
            # Fallback to hakkimizda template if not exists
            if os.path.exists('hakkimizda.html'):
                with open('hakkimizda.html', 'r', encoding='utf-8', errors='ignore') as f:
                    soup = bs4.BeautifulSoup(f.read(), 'lxml')
                panels = soup.find_all('div', class_='panel-body')
                if panels:
                    content_div = panels[-1]
                    box = content_div.find('div', class_='box')
                    new_content = bs4.BeautifulSoup(html_content, 'html.parser')
                    if box:
                        box.clear()
                        box.append(new_content)
                    else:
                        content_div.clear()
                        content_div.append(new_content)
                    headings = soup.find_all('div', class_='panel-heading')
                    if headings:
                        headings[-1].string = f'İdareci ve Bürokratlar Birliği / {title}'
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(str(soup))
                    
                    slug = filename.replace('.html', '')
                    page = Page.query.filter_by(slug=slug).first()
                    if page:
                        page.content = str(box) if box else str(panels[-1])
                    db.session.commit()

    # 1. Yonetim Kurulu
    yonkur_html = '<div class="main"><div class="panel panel-primary">'
    yonkur_html += generate_group_html('Yönetim Kurulu Üyelerimiz', groups['ya'])
    yonkur_html += generate_group_html('Yönetim Kurulu Yedek Üyelerimiz', groups['yy'])
    yonkur_html += generate_group_html('Denetleme Kurulu Üyelerimiz', groups['da'])
    yonkur_html += generate_group_html('Denetleme Kurulu Yedek Üyelerimiz', groups['dy'])
    yonkur_html += '</div></div>'
    write_to_file_and_db('yonetimkurulu.html', yonkur_html, 'Yönetim Kurulu')

    # 2. Baskanlik ve Birimler
    baskanlik_html = '<div class="main"><div class="panel panel-primary">'
    baskanlik_html += generate_group_html('Başkanlık ve Birimler', groups['br'])
    baskanlik_html += '</div></div>'
    write_to_file_and_db('baskanlik-ve-birimler.html', baskanlik_html, 'Başkanlık ve Birimler')

    # 3. Yuksek Istisare
    istisare_html = '<div class="main"><div class="panel panel-primary">'
    istisare_html += generate_group_html('Yüksek İstişare ve Onur Kurulu', groups['is'])
    istisare_html += '</div></div>'
    write_to_file_and_db('yuksek-istisare-onur-kurulu-uyesi.html', istisare_html, 'Yüksek İstişare ve Onur Kurulu')
'''

code = re.sub(r'def regenerate_yonkur_html\(\):.*?@app\.route', new_func + '\n@app.route', code, flags=re.DOTALL)
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Updated app.py successfully')
