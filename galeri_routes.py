@app.route('/admin/galeri/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_galeri_edit(id):
    g = Galeri.query.get_or_404(id)
    if request.method == 'POST':
        g.title = request.form.get('title')
        g.date = request.form.get('date')
        db.session.commit()
        return redirect(url_for('admin_galeri'))
    return render_template('admin/galeri_edit.html', galeri=g)

@app.route('/admin/galeri/sil/<int:id>', methods=['POST'])
@login_required
def admin_galeri_sil(id):
    g = Galeri.query.get_or_404(id)
    for resim in g.resimler:
        db.session.delete(resim)
    db.session.delete(g)
    db.session.commit()
    return redirect(url_for('admin_galeri'))
