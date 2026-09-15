import re

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Add apply_side_links_to_all_html
func_code = '''
def apply_side_links_to_all_html():
    import glob
    import bs4
    
    dijital = SideLink.query.filter_by(category='dijital', is_active=True).order_by(SideLink.order).all()
    gundem = SideLink.query.filter_by(category='gundem', is_active=True).order_by(SideLink.order).all()
    ebulten = SideLink.query.filter_by(category='ebulten', is_active=True).first()
    faydali = SideLink.query.filter_by(category='faydali', is_active=True).order_by(SideLink.order).all()
    
    html = ''
    
    if dijital:
        html += '<div class="panel panel-kurumsal mb-4 side-dijital"><div class="panel-heading text-center font-bold" style="background:#0f2b48; color:white; padding: 10px;">Dijital İşlemler Portalı</div><div class="panel-body text-center p-4">'
        for item in dijital:
            color = item.badge if item.badge else '#800000'
            text_color = 'white' if color == '#800000' else '#0f2b48'
            html += f'<a class="btn btn-primary w-full mb-2" href="{item.url}" style="background:{color}; border:none; display:block; padding:8px; color:{text_color}; border-radius:4px; text-decoration:none;">{item.title}</a>'
        html += '</div></div>'
        
    if gundem:
        html += '<div class="panel panel-kurumsal mb-4 side-gundem"><div class="panel-heading text-center font-bold" style="background:#0f2b48; color:white; padding: 10px;">Gündem & Buluşmalar</div><div class="panel-body p-4"><ul class="list-none p-0 m-0 text-sm">'
        for item in gundem:
            badge_html = f'<span style="background:#800000; color:white; padding:2px 6px; border-radius:4px; font-size:12px;">{item.badge}</span>' if item.badge else ''
            html += f'<li class="border-b py-2 mb-2">{badge_html} <a href="{item.url}" style="color:#0f2b48; font-weight:bold; text-decoration:none;">{item.title}</a></li>'
        html += '</ul></div></div>'
        
    if ebulten:
        html += '<div class="panel panel-kurumsal mb-4 side-ebulten"><div class="panel-heading text-center font-bold" style="background:#0f2b48; color:white; padding: 10px;">' + ebulten.title + '</div><div class="panel-body text-center p-4"><input class="form-control mb-2 p-2 border rounded w-full" placeholder="E-Posta Adresiniz" style="width:100%; box-sizing:border-box;" type="email"/><button class="btn btn-primary w-full mt-2" style="background:#800000; border:none; padding:8px; color:white; border-radius:4px; width:100%;">Abone Ol</button></div></div>'
        
    if faydali:
        html += '<div class="panel panel-cyan links side-faydali"><div class="panel-heading"><img alt="Link" src="themes/burokratlar/tema/images/icon-link.png"/>Faydalı Bağlantılar</div><div class="panel-body"><ul>'
        for item in faydali:
            html += f'<li><i aria-hidden="true" class="fa fa-link"></i> <a href="{item.url}" target="_blank">{item.title}</a></li>'
        html += '</ul></div></div>'

    for file in glob.glob('*.html') + glob.glob('haber/*.html'):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        soup = bs4.BeautifulSoup(content, 'lxml')
        left_menu_div = soup.find('div', class_='left-menu')
        
        if left_menu_div:
            # We must remove all old side blocks. They don't have a class we can target specifically except we know their structure.
            # Easiest way: remove everything in left_menu_div EXCEPT the panel-primary (Derneğimiz)
            panels_to_remove = left_menu_div.find_all('div', class_='panel', recursive=False)
            for p in panels_to_remove:
                if 'panel-primary' not in p.get('class', []):
                    p.decompose()
            
            # Now append the new html blocks
            new_blocks = bs4.BeautifulSoup(html, 'html.parser')
            for tag in new_blocks.contents:
                left_menu_div.append(tag)
                
            with open(file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
'''

text = text.replace('def apply_menus_to_all_html():', func_code + '\ndef apply_menus_to_all_html():')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Func added')
