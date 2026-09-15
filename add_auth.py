import os

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Yazar Model
old_yazar = """class Yazar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)"""

new_yazar = """class Yazar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)"""

code = code.replace(old_yazar, new_yazar)

# 2. Update login() function
old_login = """def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == '123456':
            session['logged_in'] = True
            return redirect(url_for('admin_index'))
        else:
            flash('Hatalı kullanıcı adı veya şifre')
    return render_template('login.html')"""

# We need to fetch from Setting safely
new_login = """def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check Admin
        s_user = Setting.query.get('admin_user')
        s_pass = Setting.query.get('admin_pass')
        admin_u = s_user.value if s_user and s_user.value else 'admin'
        admin_p = s_pass.value if s_pass and s_pass.value else '123456'
        
        if username == admin_u and password == admin_p:
            session['logged_in'] = True
            session.pop('yazar_id', None)
            return redirect(url_for('admin_index'))
            
        # Check Yazar
        yazar = Yazar.query.filter_by(username=username, password=password).first()
        if yazar and yazar.username:
            session['logged_in'] = True
            session['yazar_id'] = yazar.id
            return redirect(url_for('yazar_panel'))
            
        flash('Hatalı kullanıcı adı veya şifre')
    return render_template('login.html')"""

if 's_user = Setting.query.get' not in code:
    code = code.replace(old_login, new_login)

# 3. Add Yazar Panel Route and Admin Password Change Route
routes_to_add = """
@app.route('/yazar_panel')
@login_required
def yazar_panel():
    if 'yazar_id' not in session:
        return redirect(url_for('admin_index'))
    yazar = Yazar.query.get(session['yazar_id'])
    yazilar = KoseYazisi.query.filter_by(yazar_id=yazar.id).order_by(KoseYazisi.date_added.desc(), KoseYazisi.id.desc()).all()
    return render_template('admin/yazar_panel.html', yazar=yazar, yazilar=yazilar)

@app.route('/yazar_panel/ekle', methods=['POST'])
@login_required
def yazar_panel_ekle():
    if 'yazar_id' not in session: return redirect(url_for('login'))
    title = request.form.get('title')
    content = request.form.get('content')
    db.session.add(KoseYazisi(title=title, content=content, yazar_id=session['yazar_id']))
    db.session.commit()
    return redirect(url_for('yazar_panel'))

@app.route('/yazar_panel/sil/<int:id>', methods=['POST'])
@login_required
def yazar_panel_sil(id):
    if 'yazar_id' not in session: return redirect(url_for('login'))
    y = KoseYazisi.query.get(id)
    if y and y.yazar_id == session['yazar_id']:
        db.session.delete(y)
        db.session.commit()
    return redirect(url_for('yazar_panel'))

@app.route('/admin/hesap', methods=['GET', 'POST'])
@login_required
def admin_hesap():
    if 'yazar_id' in session: return redirect(url_for('yazar_panel')) # Yazar cannot change admin pass
    
    s_user = Setting.query.get('admin_user')
    s_pass = Setting.query.get('admin_pass')
    current_u = s_user.value if s_user else 'admin'
    current_p = s_pass.value if s_pass else '123456'
    
    if request.method == 'POST':
        new_u = request.form.get('username')
        new_p = request.form.get('password')
        
        if not s_user:
            s_user = Setting(key='admin_user', value=new_u)
            db.session.add(s_user)
        else:
            s_user.value = new_u
            
        if not s_pass:
            s_pass = Setting(key='admin_pass', value=new_p)
            db.session.add(s_pass)
        else:
            s_pass.value = new_p
            
        db.session.commit()
        return redirect(url_for('login')) # Re-login required
        
    return render_template('admin/hesap.html', u=current_u, p=current_p)
"""

if 'def yazar_panel():' not in code:
    code = code.replace('def admin_yazar_ekle():', routes_to_add + '\n@app.route("/admin/kose/yazar_ekle", methods=["POST"])\ndef admin_yazar_ekle():')

# 4. Update admin_yazar_ekle to accept username and password
old_ekle = """def admin_yazar_ekle():
    name = request.form.get('name')
    file = request.files.get('image')
    img_path = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        img_path = 'data/page/' + filename
    
    db.session.add(Yazar(name=name, image_path=img_path))"""

new_ekle = """def admin_yazar_ekle():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    file = request.files.get('image')
    img_path = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        img_path = 'data/page/' + filename
    
    db.session.add(Yazar(name=name, image_path=img_path, username=username, password=password))"""

code = code.replace(old_ekle, new_ekle)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.py with auth logic")
