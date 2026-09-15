import os

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

routes = """
# ================= YAZAR & KÖŞE YAZISI =================
@app.route('/admin/kose')
def admin_kose():
    yazilar = KoseYazisi.query.order_by(KoseYazisi.date_added.desc(), KoseYazisi.id.desc()).all()
    yazarlar = Yazar.query.all()
    return render_template('admin/kose_list.html', yazilar=yazilar, yazarlar=yazarlar)

@app.route('/admin/kose/yazar_ekle', methods=['POST'])
def admin_yazar_ekle():
    name = request.form.get('name')
    file = request.files.get('image')
    img_path = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        img_path = 'data/page/' + filename
    
    db.session.add(Yazar(name=name, image_path=img_path))
    db.session.commit()
    return redirect(url_for('admin_kose'))

@app.route('/admin/kose/ekle', methods=['POST'])
def admin_kose_ekle():
    title = request.form.get('title')
    content = request.form.get('content')
    yazar_id = request.form.get('yazar_id')
    
    db.session.add(KoseYazisi(title=title, content=content, yazar_id=yazar_id))
    db.session.commit()
    # In a real scenario, we'd update HTML files here too
    return redirect(url_for('admin_kose'))

@app.route('/admin/kose/sil/<int:id>', methods=['POST'])
def admin_kose_sil(id):
    y = KoseYazisi.query.get(id)
    if y:
        db.session.delete(y)
        db.session.commit()
    return redirect(url_for('admin_kose'))


# ================= GALERİ =================
@app.route('/admin/galeri')
def admin_galeri():
    galeriler = Galeri.query.all()
    return render_template('admin/galeri_list.html', galeriler=galeriler)

@app.route('/admin/galeri/ekle', methods=['POST'])
def admin_galeri_ekle():
    title = request.form.get('title')
    db.session.add(Galeri(title=title))
    db.session.commit()
    return redirect(url_for('admin_galeri'))

@app.route('/admin/galeri/<int:id>', methods=['GET', 'POST'])
def admin_galeri_detay(id):
    galeri = Galeri.query.get_or_404(id)
    if request.method == 'POST':
        files = request.files.getlist('images')
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                db.session.add(GaleriResim(galeri_id=id, image_path='data/page/'+filename))
        db.session.commit()
        return redirect(url_for('admin_galeri_detay', id=id))
        
    return render_template('admin/galeri_detay.html', galeri=galeri)

@app.route('/admin/galeri/resimsil/<int:id>', methods=['POST'])
def admin_galeri_resimsil(id):
    r = GaleriResim.query.get(id)
    gid = r.galeri_id
    if r:
        db.session.delete(r)
        db.session.commit()
    return redirect(url_for('admin_galeri_detay', id=gid))
"""

if 'def admin_kose():' not in code:
    code = code.replace('def admin_menu():', routes + '\n@app.route("/admin/menu")\ndef admin_menu():')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Routes added completely')
