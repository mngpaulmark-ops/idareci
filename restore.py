import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add EditorUser Model if missing
if 'class EditorUser(db.Model):' not in code:
    editor_model = '''class EditorUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))
    title = db.Column(db.String(100))
    role = db.Column(db.String(100))
    can_haber = db.Column(db.Boolean, default=False)
    can_etkinlik = db.Column(db.Boolean, default=False)
    can_duyuru = db.Column(db.Boolean, default=False)
    can_kose = db.Column(db.Boolean, default=False)
    can_galeri = db.Column(db.Boolean, default=False)
    can_video = db.Column(db.Boolean, default=False)

'''
    code = code.replace('class Page(db.Model):', editor_model + 'class Page(db.Model):')

# 2. Add Missing Routes
missing_routes = '''

def check_editor_permission(module):
    if session.get('role') == 'admin':
        return True
    if 'editor_id' in session:
        ed = EditorUser.query.get(session['editor_id'])
        if ed and getattr(ed, f'can_{module}', False):
            return True
    return False

@app.route('/admin/editors', methods=['GET', 'POST'])
@login_required
def admin_editors():
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))
    from werkzeug.security import generate_password_hash
    if request.method == 'POST':
        action = request.form.get('action')
        u = request.form.get('username')
        p = request.form.get('password')
        fn = request.form.get('full_name')
        ti = request.form.get('title')
        ro = request.form.get('role')
        
        ch = request.form.get('can_haber') == 'on'
        ce = request.form.get('can_etkinlik') == 'on'
        cd = request.form.get('can_duyuru') == 'on'
        ck = request.form.get('can_kose') == 'on'
        cg = request.form.get('can_galeri') == 'on'
        cv = request.form.get('can_video') == 'on'
        
        if action == 'add':
            db.session.add(EditorUser(
                username=u, password=generate_password_hash(p) if p else generate_password_hash('123456'), 
                full_name=fn, title=ti, role=ro,
                can_haber=ch, can_etkinlik=ce, can_duyuru=cd, can_kose=ck, can_galeri=cg, can_video=cv))
        elif action == 'edit':
            eid = request.form.get('editor_id')
            ed = EditorUser.query.get(eid)
            if ed:
                ed.username = u
                ed.full_name = fn
                ed.title = ti
                ed.role = ro
                ed.can_haber = ch
                ed.can_etkinlik = ce
                ed.can_duyuru = cd
                ed.can_kose = ck
                ed.can_galeri = cg
                ed.can_video = cv
                if p: ed.password = generate_password_hash(p)
        
        db.session.commit()
        return redirect(url_for('admin_editors'))
    
    editors = EditorUser.query.all()
    return render_template('admin/editors_list.html', editors=editors)

@app.route('/admin/editors/delete/<int:id>', methods=['POST'])
@login_required
def admin_editors_delete(id):
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))
    ed = EditorUser.query.get_or_404(id)
    db.session.delete(ed)
    db.session.commit()
    return redirect(url_for('admin_editors'))

@app.route('/admin/widgets', methods=['GET', 'POST'])
@login_required
def admin_widgets():
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))
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
        from flask import flash, redirect, url_for
        flash('Widget içerikleri başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_widgets'))
    return render_template('admin/widgets.html', kamu=kamu, lider=lider)

@app.route('/admin/sidebar', methods=['GET', 'POST'])
@login_required
def admin_sidebar():
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))
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
        if 'update_sidebar_html' in globals():
            threading.Thread(target=update_sidebar_html).start()
        from flask import flash, redirect, url_for
        flash('Sol menü blok görünürlükleri güncellendi.', 'success')
        return redirect(url_for('admin_sidebar'))
    return render_template('admin/sidebar_blocks.html', blocks=blocks)

@app.route('/admin/videos', methods=['GET', 'POST'])
@login_required
def admin_videos():
    if not check_editor_permission('video'): return redirect(url_for('admin_index'))
    if request.method == 'POST':
        title = request.form.get('title')
        embed = request.form.get('embed_code')
        order = request.form.get('order', type=int, default=0)
        db.session.add(Video(title=title, embed_code=embed, order=order))
        db.session.commit()
        import threading
        if 'update_video_html' in globals():
            threading.Thread(target=update_video_html).start()
        from flask import flash, redirect, url_for
        flash('Video başarıyla eklendi.', 'success')
        return redirect(url_for('admin_videos'))
    videos = Video.query.order_by(Video.order).all()
    return render_template('admin/video_list.html', videos=videos)

@app.route('/admin/videos/delete/<int:id>', methods=['POST'])
@login_required
def admin_video_delete(id):
    if not check_editor_permission('video'): return redirect(url_for('admin_index'))
    v = Video.query.get_or_404(id)
    db.session.delete(v)
    db.session.commit()
    import threading
    if 'update_video_html' in globals():
        threading.Thread(target=update_video_html).start()
    from flask import flash, redirect, url_for
    flash('Video başarıyla silindi.', 'success')
    return redirect(url_for('admin_videos'))

@app.route('/admin/left_menu', methods=['GET', 'POST'])
@login_required
def admin_left_menu():
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))
    menus = LeftMenu.query.order_by(LeftMenu.order).all()
    return render_template('admin/left_menu.html', menus=menus)

@app.route('/admin/temsilcilik')
@login_required
def admin_temsilcilik():
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))
    items = Temsilcilik.query.order_by(Temsilcilik.city_name).all()
    return render_template('admin/temsil_list.html', items=items, CITIES=CITIES)

@app.route('/admin/temsilcilik/add', methods=['GET', 'POST'])
@login_required
def admin_temsilcilik_add():
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))
    if request.method == 'POST':
        import time
        from werkzeug.utils import secure_filename
        city_code = request.form['city_code']
        city_name = CITIES.get(city_code, '')
        name = request.form['name']
        phone = request.form['phone']
        
        rep = Temsilcilik(city_code=city_code, city_name=city_name, name=name, phone=phone)
        file = request.files.get('file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            name_part, ext = os.path.splitext(filename)
            unique_filename = f"{name_part}_{int(time.time())}{ext}"
            upload_folder = os.path.join(app.root_path, 'data', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, unique_filename))
            rep.image_path = f"data/uploads/{unique_filename}"
            
        db.session.add(rep)
        db.session.commit()
        regenerate_temsilcilik_html()
        from flask import flash, redirect, url_for
        flash('Temsilcilik eklendi!')
        return redirect(url_for('admin_temsilcilik'))
    return render_template('admin/temsil_form.html', rep=None, CITIES=CITIES)

@app.route('/admin/temsilcilik/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_temsilcilik_edit(id):
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))
    rep = Temsilcilik.query.get_or_404(id)
    if request.method == 'POST':
        import time
        from werkzeug.utils import secure_filename
        rep.city_code = request.form['city_code']
        rep.city_name = CITIES.get(rep.city_code, '')
        rep.name = request.form['name']
        rep.phone = request.form['phone']
        
        file = request.files.get('file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            name_part, ext = os.path.splitext(filename)
            unique_filename = f"{name_part}_{int(time.time())}{ext}"
            upload_folder = os.path.join(app.root_path, 'data', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, unique_filename))
            rep.image_path = f"data/uploads/{unique_filename}"
            
        db.session.commit()
        regenerate_temsilcilik_html()
        from flask import flash, redirect, url_for
        flash('Temsilcilik gÃ¼ncellendi!')
        return redirect(url_for('admin_temsilcilik'))
    return render_template('admin/temsil_form.html', rep=rep, CITIES=CITIES)

@app.route('/admin/temsilcilik/delete/<int:id>', methods=['POST'])
@login_required
def admin_temsilcilik_delete(id):
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))
    rep = Temsilcilik.query.get_or_404(id)
    db.session.delete(rep)
    db.session.commit()
    regenerate_temsilcilik_html()
    from flask import flash, redirect, url_for
    flash('Temsilcilik silindi!')
    return redirect(url_for('admin_temsilcilik'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))
    return "Settings page under construction"

@app.route('/admin/haber')
@login_required
def admin_haber():
    if not check_editor_permission('haber'): return redirect(url_for('admin_index'))
    return "Haber page under construction"

'''

if 'def admin_editors():' not in code:
    code = code.replace("if __name__ == '__main__':", missing_routes + "\nif __name__ == '__main__':")


# Update the login function to handle EditorUser logic.
login_repl = """def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        s_user = Setting.query.get('admin_user')
        s_pass = Setting.query.get('admin_pass')
        admin_u = s_user.value if s_user and s_user.value else 'admin'
        admin_p = s_pass.value if s_pass and s_pass.value else '123456'
        
        if username == admin_u and password == admin_p:
            session['logged_in'] = True
            session['role'] = 'admin'
            session.pop('yazar_id', None)
            session.pop('editor_id', None)
            return redirect(url_for('admin_index'))
            
        from werkzeug.security import check_password_hash
        editor = EditorUser.query.filter_by(username=username).first()
        if editor and check_password_hash(editor.password, password):
            session['logged_in'] = True
            session['role'] = 'editor'
            session['editor_id'] = editor.id
            session.pop('yazar_id', None)
            return redirect(url_for('admin_index'))
            
        yazar = Yazar.query.filter_by(username=username, password=password).first()
        if yazar and yazar.username:
            session['logged_in'] = True
            session['role'] = 'yazar'
            session['yazar_id'] = yazar.id
            session.pop('editor_id', None)
            return redirect(url_for('yazar_panel'))
            
        flash('Hatalı giriş')
    return render_template('login.html')"""

code = re.sub(r'def login\(\):.*?(?=def logout\(\):)', login_repl + '\n\n', code, flags=re.DOTALL)

# Update admin_index to pass role and editor
admin_index_repl = """def admin_index():
    pages = Page.query.order_by(Page.menu_order).all()
    role = session.get('role')
    editor = None
    if role == 'editor' and 'editor_id' in session:
        editor = EditorUser.query.get(session['editor_id'])
    return render_template('admin/index.html', pages=pages, role=role, editor=editor)"""

code = re.sub(r'def admin_index\(\):.*?return render_template\(\'admin/index\.html\', pages=pages\)', admin_index_repl, code, flags=re.DOTALL)


# Also protect admin_edit, admin_delete, admin_add if not admin
admin_add_repl = """def admin_add():
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))"""
code = re.sub(r'def admin_add\(\):', admin_add_repl, code, count=1)

admin_edit_repl = """def admin_edit(id):
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))"""
code = re.sub(r'def admin_edit\(id\):', admin_edit_repl, code, count=1)

admin_del_repl = """def admin_delete(id):
    if session.get('role') != 'admin': return redirect(url_for('admin_index'))"""
code = re.sub(r'def admin_delete\(id\):', admin_del_repl, code, count=1)


with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Done restoring missing features.")
