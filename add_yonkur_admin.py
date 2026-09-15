import os

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add Model
yonkur_model = '''
class Yonkur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grup = db.Column(db.String(50), default='ya') # ya, yy, da, dy
    ordernum = db.Column(db.Integer, default=1)
    name = db.Column(db.String(255))
    unvan = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
'''
if 'class Yonkur' not in code:
    code = code.replace('class Page(db.Model):', yonkur_model + '\nclass Page(db.Model):')

# 2. Add Re-generator Function & Routes
yonkur_routes = '''
def regenerate_yonkur_html():
    from collections import defaultdict
    import bs4
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
                    <img src="{member['image_path']}" style="width:130px; height:130px; border-radius:50%; object-fit:cover; margin:0 auto 20px auto; border:4px solid #eaeaea; box-shadow:0 4px 10px rgba(0,0,0,0.1);" onerror="this.src='images/default-avatar.png'; this.onerror=null;">
                    <h5 style="color:#800000; font-size:17px; font-weight:700; margin-bottom:8px; line-height:1.3;">{member['name']}</h5>
                    <div style="font-size:13px; color:#666; font-weight:500; min-height:40px;">{member['unvan']}</div>
                </div>
            </div>
            """
        html += '</div></div><div class="clearfix"></div>'
        return html

    yonkur_html = '<div class="main"><div class="panel panel-primary"><div class="panel-heading" style="display:none;">Yönetim Kurulu Listesi</div>'
    yonkur_html += generate_group_html('Yönetim Kurulu Üyelerimiz', groups['ya'])
    yonkur_html += generate_group_html('Yönetim Kurulu Yedek Üyelerimiz', groups['yy'])
    yonkur_html += generate_group_html('Denetleme Kurulu Üyelerimiz', groups['da'])
    yonkur_html += generate_group_html('Denetleme Kurulu Yedek Üyelerimiz', groups['dy'])
    yonkur_html += '</div></div>'

    # Inject into template
    filename = 'yonetimkurulu.html'
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            soup = bs4.BeautifulSoup(f.read(), 'lxml')
        panels = soup.find_all('div', class_='panel-body')
        if panels:
            content_div = panels[-1]
            box = content_div.find('div', class_='box')
            new_content = bs4.BeautifulSoup(yonkur_html, 'html.parser')
            if box:
                box.clear()
                box.append(new_content)
            else:
                content_div.clear()
                content_div.append(new_content)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            page = Page.query.filter_by(slug='yonetimkurulu').first()
            if page:
                page.content = str(box) if box else str(panels[-1])
            db.session.commit()

@app.route('/admin/yonkur')
@login_required
def admin_yonkur():
    members = Yonkur.query.order_by(Yonkur.ordernum).all()
    return render_template('admin/yonkur_list.html', members=members)

@app.route('/admin/yonkur/add', methods=['GET', 'POST'])
@login_required
def admin_yonkur_add():
    if request.method == 'POST':
        import time
        from werkzeug.utils import secure_filename
        m = Yonkur()
        m.name = request.form['name']
        m.unvan = request.form['unvan']
        m.grup = request.form['grup']
        m.ordernum = int(request.form.get('ordernum', 1))
        
        file = request.files.get('file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{int(time.time())}{ext}"
            upload_folder = os.path.join(app.root_path, 'data', 'yonkur_uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            m.image_path = f'data/yonkur_uploads/{filename}'
        else:
            m.image_path = 'images/default-avatar.png'
            
        db.session.add(m)
        db.session.commit()
        regenerate_yonkur_html()
        flash('Üye eklendi!')
        return redirect(url_for('admin_yonkur'))
    return render_template('admin/yonkur_edit.html', member=None)

@app.route('/admin/yonkur/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_yonkur_edit(id):
    m = Yonkur.query.get_or_404(id)
    if request.method == 'POST':
        import time
        from werkzeug.utils import secure_filename
        m.name = request.form['name']
        m.unvan = request.form['unvan']
        m.grup = request.form['grup']
        m.ordernum = int(request.form.get('ordernum', 1))
        
        file = request.files.get('file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{int(time.time())}{ext}"
            upload_folder = os.path.join(app.root_path, 'data', 'yonkur_uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            m.image_path = f'data/yonkur_uploads/{filename}'
            
        db.session.commit()
        regenerate_yonkur_html()
        flash('Üye güncellendi!')
        return redirect(url_for('admin_yonkur'))
    return render_template('admin/yonkur_edit.html', member=m)

@app.route('/admin/yonkur/delete/<int:id>', methods=['POST'])
@login_required
def admin_yonkur_delete(id):
    m = Yonkur.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    regenerate_yonkur_html()
    flash('Üye silindi!')
    return redirect(url_for('admin_yonkur'))

'''
if '/admin/yonkur' not in code:
    code = code.replace("if __name__ == '__main__':", yonkur_routes + "\nif __name__ == '__main__':")
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("app.py updated with Yonkur routes")
