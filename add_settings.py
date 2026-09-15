import os

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

settings_model = """
class Setting(db.Model):
    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Text, nullable=True)
"""

if 'class Setting(db.Model):' not in code:
    code = code.replace('class Haber(db.Model):', settings_model + '\nclass Haber(db.Model):')

settings_routes = """
@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    keys = [
        ('facebook_url', 'Facebook Adresi', '#facebook'),
        ('twitter_url', 'Twitter Adresi', '#twitter'),
        ('instagram_url', 'Instagram Adresi', '#'),
        ('youtube_url', 'YouTube Adresi', '#'),
        ('footer_copyright', 'Footer Telif Yazısı', '© 2015 İdareci ve Bürokratlar Birliği Derneği Tüm Hakları Saklıdır.'),
        ('contact_address', 'İletişim - Adres', ''),
        ('contact_phone', 'İletişim - Telefon', ''),
        ('contact_email', 'İletişim - E-posta', '')
    ]
    
    if request.method == 'POST':
        for key, _, _ in keys:
            val = request.form.get(key, '')
            s = Setting.query.get(key)
            if s:
                s.value = val
            else:
                db.session.add(Setting(key=key, value=val))
        db.session.commit()
        
        apply_settings_to_all_html()
        return redirect(url_for('admin_settings'))
        
    settings = {}
    for key, label, default in keys:
        s = Setting.query.get(key)
        settings[key] = {
            'label': label,
            'value': s.value if s else default
        }
        
    return render_template('admin/settings.html', settings=settings)

def apply_settings_to_all_html():
    import glob
    import bs4
    
    def get_val(k, default=''):
        s = Setting.query.get(k)
        return s.value if s and s.value else default

    fb = get_val('facebook_url', '#facebook')
    tw = get_val('twitter_url', '#twitter')
    ig = get_val('instagram_url', '#')
    yt = get_val('youtube_url', '#')
    copy = get_val('footer_copyright', '© 2015 İdareci ve Bürokratlar Birliği Derneği Tüm Hakları Saklıdır.')
    address = get_val('contact_address', '')
    phone = get_val('contact_phone', '')
    email = get_val('contact_email', '')
    
    for file in glob.glob('*.html') + glob.glob('haber/*.html'):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        soup = bs4.BeautifulSoup(content, 'lxml')
        
        changed = False
        
        # Social Links
        for a in soup.find_all('a', href=True):
            if a.find('img') and a.find('img').get('src'):
                src = a.find('img')['src']
                if 'icon-facebook' in src:
                    a['href'] = fb
                    changed = True
                elif 'icon-twitter' in src:
                    a['href'] = tw
                    changed = True
                elif 'icon-instagram' in src: # assuming they have or add one
                    a['href'] = ig
                    changed = True
                elif 'icon-youtube' in src:
                    a['href'] = yt
                    changed = True
                    
        # Copyright Text
        footer = soup.find('div', class_='footer-bottom')
        if footer:
            p = footer.find('p')
            if p:
                p.string = copy
                changed = True
                
        # If it's iletisim.html, we can update contact details
        if 'iletisim.html' in file:
            # Finding address/phone elements is hard without id, we will just pass for now or look for specific panels
            pass
            
        if changed:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
"""

if 'def admin_settings():' not in code:
    code = code.replace('def admin_haber():', settings_routes + '\ndef admin_haber():')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.py with Setting model")
