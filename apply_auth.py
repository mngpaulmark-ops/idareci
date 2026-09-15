import os
import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Replace Yazar Model
code = re.sub(r'class Yazar\(db\.Model\):.*?image_path = db\.Column\(db\.String\(255\), nullable=True\)', 
'''class Yazar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)''', code, flags=re.DOTALL)

# 2. Replace login()
login_pattern = r'def login\(\):.*?return render_template\(\'login\.html\'\)'
new_login = '''def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        s_user = Setting.query.get('admin_user')
        s_pass = Setting.query.get('admin_pass')
        admin_u = s_user.value if s_user and s_user.value else 'admin'
        admin_p = s_pass.value if s_pass and s_pass.value else '123456'
        
        if username == admin_u and password == admin_p:
            session['logged_in'] = True
            session.pop('yazar_id', None)
            return redirect(url_for('admin_index'))
            
        yazar = Yazar.query.filter_by(username=username, password=password).first()
        if yazar and yazar.username:
            session['logged_in'] = True
            session['yazar_id'] = yazar.id
            return redirect(url_for('yazar_panel'))
            
        flash('Hatalı giriş')
    return render_template('login.html')'''
code = re.sub(login_pattern, new_login, code, flags=re.DOTALL)

# 3. Add Yazar Panel and Admin Pass logic
routes = '''
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
    if 'yazar_id' in session: return redirect(url_for('yazar_panel'))
    
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
        return redirect(url_for('login'))
        
    return render_template('admin/hesap.html', u=current_u, p=current_p)
'''
if 'def yazar_panel():' not in code:
    code = code.replace('@app.route(\'/admin/kose/yazar_ekle\', methods=[\'POST\'])', routes + '\\n@app.route(\'/admin/kose/yazar_ekle\', methods=[\'POST\'])')

# 4. Fix admin_yazar_ekle
code = code.replace('db.session.add(Yazar(name=name, image_path=img_path))', 
                    'db.session.add(Yazar(name=name, image_path=img_path, username=request.form.get("username"), password=request.form.get("password")))')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Regex replace done.')
