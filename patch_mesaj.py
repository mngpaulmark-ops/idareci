import re

with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Add Mesaj model
mesaj_model = """
class Mesaj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
"""
if 'class Mesaj(db.Model):' not in content:
    content = content.replace('class Page(db.Model):', mesaj_model + '\n\nclass Page(db.Model):')

# 2. Add routes
mesaj_routes = """
@app.route('/iletisim/gonder', methods=['POST'])
def iletisim_gonder():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    comment = request.form.get('comment')
    if name and email and comment:
        yeni = Mesaj(name=name, phone=phone, email=email, comment=comment)
        db.session.add(yeni)
        db.session.commit()
        return "<script>alert('Mesajınız başarıyla gönderilmiştir. Teşekkür ederiz.'); window.location.href='/iletisim.html';</script>"
    return "<script>alert('Lütfen tüm zorunlu alanları doldurun.'); window.history.back();</script>"

@app.route('/admin/mesajlar')
@login_required
def admin_mesajlar():
    if session.get('role') != 'admin':
        return redirect(url_for('admin_index'))
    mesajlar = Mesaj.query.order_by(Mesaj.date_added.desc()).all()
    return render_template('admin/mesajlar.html', mesajlar=mesajlar)

@app.route('/admin/mesajlar/sil/<int:id>', methods=['POST'])
@login_required
def admin_mesaj_sil(id):
    if session.get('role') != 'admin':
        return redirect(url_for('admin_index'))
    m = Mesaj.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    flash('Mesaj silindi!')
    return redirect(url_for('admin_mesajlar'))

@app.route('/admin/mesajlar/oku/<int:id>', methods=['POST'])
@login_required
def admin_mesaj_oku(id):
    if session.get('role') != 'admin':
        return redirect(url_for('admin_index'))
    m = Mesaj.query.get_or_404(id)
    m.is_read = True
    db.session.commit()
    flash('Mesaj okundu olarak işaretlendi.')
    return redirect(url_for('admin_mesajlar'))
"""
if "def iletisim_gonder():" not in content:
    content = content + "\n\n" + mesaj_routes

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
