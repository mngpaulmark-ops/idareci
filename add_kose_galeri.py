import os

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

models = """
class Yazar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)

class KoseYazisi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    yazar_id = db.Column(db.Integer, db.ForeignKey('yazar.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    yazar = db.relationship('Yazar', backref=db.backref('yazilar', lazy=True))

class Galeri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    
class GaleriResim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    galeri_id = db.Column(db.Integer, db.ForeignKey('galeri.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    
    galeri = db.relationship('Galeri', backref=db.backref('resimler', lazy=True))
"""

if 'class Yazar(db.Model):' not in code:
    code = code.replace('class Menu(db.Model):', models + '\nclass Menu(db.Model):')

routes = """
@app.route('/admin/yazar')
def admin_yazar():
    return render_template('admin/yazar_list.html', yazarlar=Yazar.query.all())

@app.route('/admin/galeri')
def admin_galeri():
    return render_template('admin/galeri_list.html', galeriler=Galeri.query.all())
"""

if 'def admin_yazar():' not in code:
    code = code.replace('def admin_menu():', routes + '\n@app.route("/admin/menu")\ndef admin_menu():')
    
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Models and basic routes added')
