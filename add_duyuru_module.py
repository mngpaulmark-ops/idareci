import os, sys

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add Duyuru Model
duyuru_model = """
class Duyuru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class EditorUser(db.Model):"""

code = code.replace("class EditorUser(db.Model):", duyuru_model)


# 2. Add Routes
duyuru_routes = """
@app.route('/admin/duyuru')
@login_required
def admin_duyuru():
    duyurular = Duyuru.query.order_by(Duyuru.date_added.desc(), Duyuru.id.desc()).all()
    return render_template('admin/duyuru_list.html', duyurular=duyurular)

@app.route('/admin/duyuru/add', methods=['GET', 'POST'])
@login_required
def admin_duyuru_add():
    if request.method == 'POST':
        t = request.form.get('title')
        l = request.form.get('link')
        d = Duyuru(title=t, link=l)
        db.session.add(d)
        db.session.commit()
        
        # Regenerate front page
        try:
            import subprocess
            subprocess.run(['python', 'update_anasayfa.py'])
        except:
            pass
            
        flash('Duyuru eklendi.', 'success')
        return redirect(url_for('admin_duyuru'))
    return render_template('admin/duyuru_edit.html')

@app.route('/admin/duyuru/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_duyuru_edit(id):
    d = Duyuru.query.get_or_404(id)
    if request.method == 'POST':
        d.title = request.form.get('title')
        d.link = request.form.get('link')
        db.session.commit()
        
        # Regenerate front page
        try:
            import subprocess
            subprocess.run(['python', 'update_anasayfa.py'])
        except:
            pass
            
        flash('Duyuru güncellendi.', 'success')
        return redirect(url_for('admin_duyuru'))
    return render_template('admin/duyuru_edit.html', duyuru=d)

@app.route('/admin/duyuru/delete/<int:id>', methods=['POST'])
@login_required
def admin_duyuru_delete(id):
    d = Duyuru.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    
    # Regenerate front page
    try:
        import subprocess
        subprocess.run(['python', 'update_anasayfa.py'])
    except:
        pass
        
    flash('Duyuru silindi.', 'success')
    return redirect(url_for('admin_duyuru'))

# ================= EDITOR USER MODEL & ROUTES =================
"""

code = code.replace("# ================= EDITOR USER MODEL & ROUTES =================", duyuru_routes)


with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Added Duyuru model and routes!")
