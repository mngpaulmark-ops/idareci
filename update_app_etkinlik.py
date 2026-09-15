import re
with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

etkinlik_routes = '''
@app.route('/admin/etkinlik')
@login_required
def admin_etkinlik():
    etkinlikler = Etkinlik.query.order_by(Etkinlik.id.desc()).all()
    return render_template('admin/etkinlik_list.html', etkinlikler=etkinlikler)

@app.route('/admin/etkinlik/ekle', methods=['GET', 'POST'])
@login_required
def admin_etkinlik_ekle():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        edate = request.form.get('edate')
        saat = request.form.get('saat')
        
        yeni = Etkinlik(title=title, description=description, edate=edate, saat=saat)
        db.session.add(yeni)
        db.session.commit()
        import etkinlik_helper
        etkinlik_helper.regenerate_anasayfa_etkinlikler()
        return redirect(url_for('admin_etkinlik'))
    return render_template('admin/etkinlik_edit.html', etkinlik=None)

@app.route('/admin/etkinlik/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_etkinlik_edit(id):
    etkinlik = Etkinlik.query.get_or_404(id)
    if request.method == 'POST':
        etkinlik.title = request.form.get('title')
        etkinlik.description = request.form.get('description')
        etkinlik.edate = request.form.get('edate')
        etkinlik.saat = request.form.get('saat')
        db.session.commit()
        import etkinlik_helper
        etkinlik_helper.regenerate_anasayfa_etkinlikler()
        return redirect(url_for('admin_etkinlik'))
    return render_template('admin/etkinlik_edit.html', etkinlik=etkinlik)

@app.route('/admin/etkinlik/sil/<int:id>', methods=['POST'])
@login_required
def admin_etkinlik_sil(id):
    etkinlik = Etkinlik.query.get_or_404(id)
    db.session.delete(etkinlik)
    db.session.commit()
    import etkinlik_helper
    etkinlik_helper.regenerate_anasayfa_etkinlikler()
    return redirect(url_for('admin_etkinlik'))

'''

text = text.replace('@app.route(\'/admin/galeri\')', etkinlik_routes + '\n@app.route(\'/admin/galeri\')')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Etkinlik routes added.')
