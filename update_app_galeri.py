import re

with open('app.py', 'r', encoding='utf-8', errors='surrogateescape') as f:
    code = f.read()

# Update Model
if 'date = db.Column(db.String(50))' not in code:
    code = code.replace("title = db.Column(db.String(100), nullable=False)", "title = db.Column(db.String(100), nullable=False)\n    date = db.Column(db.String(50))\n    location = db.Column(db.String(100))")

# Update admin_galeri_ekle
if 'date = request.form.get(\'date\')' not in code:
    code = code.replace("title = request.form.get('title')\n    db.session.add(Galeri(title=title))", "title = request.form.get('title')\n    date = request.form.get('date')\n    location = request.form.get('location')\n    db.session.add(Galeri(title=title, date=date, location=location))")

# Update admin_galeri_detay
detay_patch = """    if request.method == 'POST':
        # Also update metadata if submitted
        if 'title' in request.form:
            galeri.title = request.form.get('title')
            galeri.date = request.form.get('date')
            galeri.location = request.form.get('location')
            db.session.commit()
"""
if "if 'title' in request.form:" not in code:
    code = code.replace("    if request.method == 'POST':\n        files = request.files.getlist('images')", detay_patch + "        files = request.files.getlist('images')")
    
# After saving images or gallery info, we should regenerate resimler.html
# Add import galeri_helper and trigger it
regenerate_call = """        import threading\n        try:\n            import galeri_helper\n            threading.Thread(target=galeri_helper.regenerate_resimler_html).start()\n        except:\n            pass\n"""

# Inject into admin_galeri_ekle
code = re.sub(r'(def admin_galeri_ekle\(\):.*?db\.session\.commit\(\))', r'\1\n' + regenerate_call, code, flags=re.DOTALL)

# Inject into admin_galeri_detay (after commit of form data or after image upload)
# This gets tricky, better to just let galeri_helper handle regeneration and we can manually call it.
# Wait, I will just create `galeri_helper.py` and call it.
code = code.replace("flash('Resimler eklendi.', 'success')", "flash('Resimler eklendi.', 'success')\n" + regenerate_call)
code = code.replace("def admin_galeri_resimsil(id):\n    r = GaleriResim.query.get(id)\n    gid = r.galeri_id\n    if r:\n        db.session.delete(r)\n        db.session.commit()", "def admin_galeri_resimsil(id):\n    if not check_editor_permission('galeri'): return redirect(url_for('admin_index'))\n    r = GaleriResim.query.get(id)\n    gid = r.galeri_id\n    if r:\n        db.session.delete(r)\n        db.session.commit()\n" + regenerate_call)


with open('app.py', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(code)

print("Updated app.py Galeri model and routes.")
