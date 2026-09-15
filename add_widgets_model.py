import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

model_code = '''
class WidgetContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    link = db.Column(db.String(255))
'''

content = content.replace('class LeftMenu(db.Model):', model_code + '\nclass LeftMenu(db.Model):')

# Add admin route
admin_route = '''
@app.route('/admin/widgets', methods=['GET', 'POST'])
@login_required
def admin_widgets():
    kamu = WidgetContent.query.filter_by(slug='kamu-etigi').first()
    lider = WidgetContent.query.filter_by(slug='yonetim-liderlik').first()
    
    if not kamu:
        kamu = WidgetContent(slug='kamu-etigi', title='Kamu Etiği ve Yönetim İlkeleri', description='Kamuda etik değerler ve şeffaf yönetim anlayışı üzerine düzenlenen güncel seminer programlarımız.', link='#')
        db.session.add(kamu)
    if not lider:
        lider = WidgetContent(slug='yonetim-liderlik', title='Yönetim ve Liderlik Seminerleri', description='Geleceğin yöneticilerini yetiştiren vizyoner liderlik eğitimleri ve akademik panel serileri.', link='#')
        db.session.add(lider)
    db.session.commit()
    
    if request.method == 'POST':
        kamu.title = request.form.get('kamu_title')
        kamu.description = request.form.get('kamu_desc')
        kamu.link = request.form.get('kamu_link')
        
        lider.title = request.form.get('lider_title')
        lider.description = request.form.get('lider_desc')
        lider.link = request.form.get('lider_link')
        
        db.session.commit()
        
        # Update HTML in background
        import threading
        threading.Thread(target=update_widgets_html).start()
        
        flash('Widget içerikleri başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_widgets'))
        
    return render_template('admin/widgets.html', kamu=kamu, lider=lider)

def update_widgets_html():
    with app.app_context():
        import bs4
        import glob
        kamu = WidgetContent.query.filter_by(slug='kamu-etigi').first()
        lider = WidgetContent.query.filter_by(slug='yonetim-liderlik').first()
        
        if not kamu or not lider: return
        
        for file in glob.glob('anasayfa.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            soup = bs4.BeautifulSoup(content, 'lxml')
            
            p_kamu = soup.find('div', id='panel-kamu-etigi')
            if p_kamu:
                p_kamu.find('p').string = kamu.description
                btn = p_kamu.find('a', class_='btn')
                if btn:
                    btn['href'] = kamu.link
                    # Update text without removing icon
                    icon = btn.find('i')
                    btn.clear()
                    btn.append("Detayları İncele ")
                    if icon: btn.append(icon)
                    
            p_lider = soup.find('div', id='panel-yonetim-liderlik')
            if p_lider:
                p_lider.find('p').string = lider.description
                btn = p_lider.find('a', class_='btn')
                if btn:
                    btn['href'] = lider.link
                    icon = btn.find('i')
                    btn.clear()
                    btn.append("Seminerlere Git ")
                    if icon: btn.append(icon)
                    
            with open(file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
'''

# insert route near admin_haber
content = content.replace('@app.route(\'/admin/haber\')', admin_route + '\n@app.route(\'/admin/haber\')')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py with Widget model and routes.")
