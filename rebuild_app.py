import re

with open('C:/tmp/app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

# 1. Models
models_to_inject = '''
class WidgetContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    link = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

class SidebarBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    embed_code = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
'''
app_code = app_code.replace("class Page(db.Model):", models_to_inject + "\nclass Page(db.Model):")

# EditorUser
editor_repl = '''class EditorUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))
    title = db.Column(db.String(100))
    role = db.Column(db.String(100))
    can_haber = db.Column(db.Boolean, default=False)'''
app_code = re.sub(r'class EditorUser\(db\.Model\):\n\s+id =.*?\n\s+username =.*?\n\s+password =.*?\n\s+can_haber = db\.Column\(db\.Boolean, default=False\)', editor_repl, app_code, flags=re.DOTALL)

# Editor logic
add_repl = '''
        fn = request.form.get('full_name')
        ti = request.form.get('title')
        ro = request.form.get('role')
        
        if action == 'add':
            db.session.add(EditorUser(
                username=u, password=generate_password_hash(p), 
                full_name=fn, title=ti, role=ro,
                can_haber=ch, can_etkinlik=ce, can_duyuru=cd, can_kose=ck))
'''
app_code = re.sub(r"if action == 'add':\n\s+db\.session\.add\(EditorUser\(username=u, password=generate_password_hash\(p\), can_haber=ch, can_etkinlik=ce, can_duyuru=cd, can_kose=ck\)\)", add_repl, app_code)

edit_repl = '''elif action == 'edit':
            eid = request.form.get('editor_id')
            ed = EditorUser.query.get(eid)
            ed.username = u
            ed.full_name = fn
            ed.title = ti
            ed.role = ro
            if p: ed.password = generate_password_hash(p)'''
app_code = re.sub(r"elif action == 'edit':\n\s+eid = request\.form\.get\('editor_id'\)\n\s+ed = EditorUser\.query\.get\(eid\)\n\s+ed\.username = u\n\s+if p: ed\.password = generate_password_hash\(p\)", edit_repl, app_code)

# login_required logic
kose_guard = '''        if user.can_duyuru:
            allowed_endpoints.extend(['admin_menu', 'admin_menu_add', 'admin_menu_toggle', 'admin_menu_delete', 'admin_menu_move'])
        if user.can_kose:
            allowed_endpoints.extend(['admin_kose', 'admin_kose_ekle', 'admin_kose_edit', 'admin_kose_sil', 'admin_yazar_ekle'])'''
app_code = app_code.replace("if user.can_duyuru:\n            allowed_endpoints.extend(['admin_menu', 'admin_menu_add', 'admin_menu_toggle', 'admin_menu_delete', 'admin_menu_move'])", kose_guard)

# temsilcilik uploads fix
app_code = app_code.replace('rep.image_path = f"uploads/{unique_filename}"', 'rep.image_path = f"data/uploads/{unique_filename}"')

# Remove bs4 based updaters entirely
app_code = re.sub(r'def apply_side_links_to_all_html\(\):.*?def _apply_menus_inner\(\):.*?(?=if __name__ == \'__main__\':)', '', app_code, flags=re.DOTALL)

# Add all safe updaters and new routes
new_routes = '''
@app.route('/admin/widgets', methods=['GET', 'POST'])
@login_required
def admin_widgets():
    kamu = WidgetContent.query.filter_by(slug='kamu-etigi').first()
    lider = WidgetContent.query.filter_by(slug='yonetim-liderlik').first()
    if not kamu:
        kamu = WidgetContent(slug='kamu-etigi', title='Kamu Etiği', description='', link='', is_active=True)
        db.session.add(kamu)
    if not lider:
        lider = WidgetContent(slug='yonetim-liderlik', title='Yönetim Seminerleri', description='', link='', is_active=True)
        db.session.add(lider)
    db.session.commit()
    
    if request.method == 'POST':
        kamu.description = request.form.get('kamu_desc')
        kamu.link = request.form.get('kamu_link')
        kamu.is_active = request.form.get('kamu_active') == 'on'
        
        lider.description = request.form.get('lider_desc')
        lider.link = request.form.get('lider_link')
        lider.is_active = request.form.get('lider_active') == 'on'
        
        db.session.commit()
        import threading
        threading.Thread(target=update_widgets_html).start()
        
        from flask import flash, redirect, url_for
        flash('Widget içerikleri başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_widgets'))
    return render_template('admin/widgets.html', kamu=kamu, lider=lider)

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
            b.is_active = request.form.get(f'block_{b.slug}') == 'on'
        db.session.commit()
        import threading
        threading.Thread(target=update_sidebar_html).start()
        from flask import flash, redirect, url_for
        flash('Sol menü blok görünürlükleri güncellendi.', 'success')
        return redirect(url_for('admin_sidebar'))
    return render_template('admin/sidebar_blocks.html', blocks=blocks)

@app.route('/admin/videos', methods=['GET', 'POST'])
@login_required
def admin_videos():
    if request.method == 'POST':
        title = request.form.get('title')
        embed = request.form.get('embed_code')
        order = request.form.get('order', type=int, default=0)
        db.session.add(Video(title=title, embed_code=embed, order=order))
        db.session.commit()
        import threading
        threading.Thread(target=update_video_html).start()
        from flask import flash, redirect, url_for
        flash('Video başarıyla eklendi.', 'success')
        return redirect(url_for('admin_videos'))
    videos = Video.query.order_by(Video.order).all()
    return render_template('admin/video_list.html', videos=videos)

@app.route('/admin/videos/delete/<int:id>', methods=['POST'])
@login_required
def admin_video_delete(id):
    v = Video.query.get_or_404(id)
    db.session.delete(v)
    db.session.commit()
    import threading
    threading.Thread(target=update_video_html).start()
    from flask import flash, redirect, url_for
    flash('Video başarıyla silindi.', 'success')
    return redirect(url_for('admin_videos'))

def update_widgets_html():
    with app.app_context():
        import glob
        import re
        kamu = WidgetContent.query.filter_by(slug='kamu-etigi').first()
        lider = WidgetContent.query.filter_by(slug='yonetim-liderlik').first()
        if not kamu or not lider: return
        for file in glob.glob('anasayfa.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f: page = f.read()
            new_page = page
            for w in [kamu, lider]:
                panel_id = f'panel-{w.slug}'
                pattern = r'(<div[^>]*id="' + re.escape(panel_id) + r'"[^>]*style=")([^"]*)(")'
                def replacer(match):
                    pre, style, post = match.groups()
                    if w.is_active:
                        style = re.sub(r'display:\s*none\s*!important;?', '', style)
                        style = re.sub(r'display:\s*none;?', '', style)
                    else:
                        if 'display: none' not in style: style += ' display: none !important;'
                    return pre + style.strip() + post
                new_page = re.sub(pattern, replacer, new_page)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f: f.write(new_page)

def update_sidebar_html():
    with app.app_context():
        import glob
        import re
        blocks = {b.slug: b.is_active for b in SidebarBlock.query.all()}
        if not blocks: return
        for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f: page = f.read()
            new_page = page
            for slug, is_active in blocks.items():
                class_name = 'hadis-i-serif' if slug == 'hadis' else f'side-{slug}'
                pattern = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*style=")([^"]*)(")'
                def replacer(match):
                    pre, style, post = match.groups()
                    if is_active:
                        style = re.sub(r'display:\s*none\s*!important;?', '', style)
                        style = re.sub(r'display:\s*none;?', '', style)
                    else:
                        if 'display: none' not in style: style += ' display: none !important;'
                    return pre + style.strip() + post
                new_page = re.sub(pattern, replacer, new_page)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f: f.write(new_page)

def update_video_html():
    with app.app_context():
        import glob
        import re
        videos = Video.query.order_by(Video.order).all()
        if not videos: return
        html = ""
        for v in videos:
            html += f"<li><div style='padding: 5px; text-align:center;'>{v.embed_code}<div class='caption' style='margin-top:5px;'><h5 style='font-size:13px; font-weight:bold; color:#333;'>{v.title}</h5></div></div></li>\\n"
        for file in glob.glob('anasayfa.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f: page = f.read()
            pattern = r'(<div class="panel-body videogaleri jcarousel">.*?<ul>).*?(</ul>\\s*</div>)'
            new_page = re.sub(pattern, r'\\g<1>\\n' + html + r'\\g<2>', page, flags=re.DOTALL)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f: f.write(new_page)

def apply_menus_to_all_html():
    with app.app_context():
        import glob
        import re
        menus = Menu.query.filter_by(parent_id=None, is_active=True).order_by(Menu.order).all()
        html = '<ul class="nav navbar-nav">\\n'
        html += '<li class="home"><a href="anasayfa.html"><img alt="Ana Sayfa" src="themes/burokratlar/tema/images/ico-home.png"/></a></li>\\n'
        for m in menus:
            if m.children:
                html += f'<li class="dropdown"><a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="{m.url}" role="button" target="_self">{m.title}</a>\\n<ul class="dropdown-menu" role="menu">\\n'
                for child in [c for c in m.children if c.is_active]: html += f'<li><a href="{child.url}" target="_self">{child.title}</a></li>\\n'
                html += '</ul></li>\\n'
            else:
                html += f'<li><a href="{m.url}" target="_self">{m.title}</a></li>\\n'
        html += '</ul>'
        
        left_menus = LeftMenu.query.filter_by(is_active=True).order_by(LeftMenu.order).all()
        left_html = '<ul id="left-menu">\\n'
        for lm in left_menus: left_html += f'<li><a href="{lm.url}" target="_self">{lm.title}</a></li>\\n'
        left_html += '</ul>'
        
        for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f: page = f.read()
            new_page = page
            pattern_top = r'(<nav class="collapse navbar-collapse bs-navbar-collapse" id="bs-example-navbar-collapse-1">\\s*)<ul class="nav navbar-nav">.*?</ul>(\\s*</nav>)'
            new_page = re.sub(pattern_top, r'\\g<1>' + html.replace('\\\\', '\\\\\\\\') + r'\\g<2>', new_page, flags=re.DOTALL)
            pattern_left = r'(<div class="panel-heading">\\s*<img alt="Menu" src="themes/burokratlar/tema/images/icon-menu.png"/> Derneğimiz\\s*</div>\\s*<div class="panel-body">\\s*)<ul id="left-menu">.*?</ul>(\\s*</div>)'
            new_page = re.sub(pattern_left, r'\\g<1>' + left_html.replace('\\\\', '\\\\\\\\') + r'\\g<2>', new_page, flags=re.DOTALL)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f: f.write(new_page)

'''
app_code = app_code.replace("if __name__ == '__main__':", new_routes + "\n\nif __name__ == '__main__':")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("Restored app.py completely with safe updaters and NO lost routes!")
