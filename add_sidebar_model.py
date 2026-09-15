import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

model_code = '''
class SidebarBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
'''

content = content.replace('class WidgetContent(db.Model):', model_code + '\nclass WidgetContent(db.Model):')

admin_route = '''
@app.route('/admin/sidebar', methods=['GET', 'POST'])
@login_required
def admin_sidebar():
    blocks_data = [
        ('hadis', 'Günün Hadis-i Şerifi'),
        ('dijital', 'Dijital İşlemler Portalı'),
        ('gundem', 'Gündem & Buluşmalar'),
        ('ebulten', 'E-Bülten & Politika Notları'),
        ('faydali', 'Faydalı Bağlantılar'),
        ('banner', 'Milli İrade Platformu Banner')
    ]
    
    for slug, title in blocks_data:
        if not SidebarBlock.query.filter_by(slug=slug).first():
            db.session.add(SidebarBlock(slug=slug, title=title, is_active=True))
    db.session.commit()
    
    blocks = SidebarBlock.query.order_by(SidebarBlock.id).all()
    
    if request.method == 'POST':
        for b in blocks:
            # Checkbox values are only in request.form if checked
            b.is_active = request.form.get(f'block_{b.slug}') == 'on'
        db.session.commit()
        
        # Update HTML in background
        import threading
        threading.Thread(target=update_sidebar_html).start()
        
        flash('Sol menü blok görünürlükleri güncellendi.', 'success')
        return redirect(url_for('admin_sidebar'))
        
    return render_template('admin/sidebar_blocks.html', blocks=blocks)

def _toggle_display(element, is_active):
    if not element: return
    style = element.get('style', '')
    if is_active:
        style = re.sub(r'display:\s*none\s*!important;?', '', style)
        style = re.sub(r'display:\s*none;?', '', style)
    else:
        if 'display: none' not in style:
            style += ' display: none !important;'
    element['style'] = style.strip()

def update_sidebar_html():
    with app.app_context():
        import bs4
        import glob
        blocks = {b.slug: b.is_active for b in SidebarBlock.query.all()}
        if not blocks: return
        
        for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            soup = bs4.BeautifulSoup(content, 'lxml')
            
            # Hadis
            hadis = soup.find(lambda tag: tag.name == 'div' and 'Günün Hadis-i Şerifi' in tag.get_text() and 'panel' in tag.get('class', []))
            if hadis: _toggle_display(hadis, blocks.get('hadis', True))
            
            # Dijital
            dijital = soup.find('div', class_='side-dijital')
            if dijital: _toggle_display(dijital, blocks.get('dijital', True))
            
            # Gundem
            gundem = soup.find('div', class_='side-gundem')
            if gundem: _toggle_display(gundem, blocks.get('gundem', True))
            
            # Ebulten
            ebulten = soup.find('div', class_='side-ebulten')
            if ebulten: _toggle_display(ebulten, blocks.get('ebulten', True))
            
            # Faydali
            faydali = soup.find('div', class_='side-faydali')
            if faydali: _toggle_display(faydali, blocks.get('faydali', True))
            
            # Banner
            banner = soup.find('div', id='yanaplat-banner')
            if banner: _toggle_display(banner, blocks.get('banner', True))
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
'''

content = content.replace('@app.route(\'/admin/haber\')', admin_route + '\n@app.route(\'/admin/haber\')')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added SidebarBlock model and routes.")
