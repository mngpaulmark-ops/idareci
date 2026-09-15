import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

haber_routes = '''
@app.route('/admin/haber')
@login_required
def admin_haber():
    if not check_editor_permission('haber'): return redirect(url_for('admin_index'))
    habers = Haber.query.order_by(Haber.id.desc()).all()
    return render_template('admin/haber_list.html', habers=habers)

@app.route('/admin/haber/add', methods=['GET', 'POST'])
@login_required
def admin_haber_add():
    if not check_editor_permission('haber'): return redirect(url_for('admin_index'))
    if request.method == 'POST':
        import time
        from werkzeug.utils import secure_filename
        title = request.form.get('title')
        content = request.form.get('content')
        slug = request.form.get('slug', '')
        if not slug:
            # Generate basic slug
            slug = title.lower().replace(' ', '-').replace('ı', 'i').replace('ö', 'o').replace('ü', 'u').replace('ş', 's').replace('ğ', 'g').replace('ç', 'c')
            slug = "".join(c for c in slug if c.isalnum() or c == '-')
        
        h = Haber(title=title, content=content, slug=slug)
        file = request.files.get('image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            name_part, ext = os.path.splitext(filename)
            unique_filename = f"{name_part}_{int(time.time())}{ext}"
            upload_folder = os.path.join(app.root_path, 'data', 'haber_uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, unique_filename))
            h.image_path = f"data/haber_uploads/{unique_filename}"
            
        db.session.add(h)
        db.session.commit()
        
        try:
            import haber_helper
            haber_helper.regenerate_haber_html(h)
            haber_helper.regenerate_haber_listesi()
            import etkinlik_helper
            etkinlik_helper.regenerate_anasayfa_etkinlikler()
        except:
            pass
            
        from flask import flash
        flash('Haber başarıyla eklendi!')
        return redirect(url_for('admin_haber'))
    return render_template('admin/haber_edit.html', haber=None)

@app.route('/admin/haber/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_haber_edit(id):
    if not check_editor_permission('haber'): return redirect(url_for('admin_index'))
    h = Haber.query.get_or_404(id)
    if request.method == 'POST':
        import time
        from werkzeug.utils import secure_filename
        h.title = request.form.get('title')
        h.content = request.form.get('content')
        h.slug = request.form.get('slug')
        
        file = request.files.get('image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            name_part, ext = os.path.splitext(filename)
            unique_filename = f"{name_part}_{int(time.time())}{ext}"
            upload_folder = os.path.join(app.root_path, 'data', 'haber_uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, unique_filename))
            h.image_path = f"data/haber_uploads/{unique_filename}"
            
        db.session.commit()
        
        try:
            import haber_helper
            haber_helper.regenerate_haber_html(h)
            haber_helper.regenerate_haber_listesi()
            import etkinlik_helper
            etkinlik_helper.regenerate_anasayfa_etkinlikler()
        except:
            pass
            
        from flask import flash
        flash('Haber güncellendi!')
        return redirect(url_for('admin_haber'))
    return render_template('admin/haber_edit.html', haber=h)

@app.route('/admin/haber/delete/<int:id>', methods=['POST'])
@login_required
def admin_haber_delete(id):
    if not check_editor_permission('haber'): return redirect(url_for('admin_index'))
    h = Haber.query.get_or_404(id)
    db.session.delete(h)
    db.session.commit()
    
    try:
        import haber_helper
        haber_helper.regenerate_haber_listesi()
        import etkinlik_helper
        etkinlik_helper.regenerate_anasayfa_etkinlikler()
    except:
        pass
        
    import os
    file_path = os.path.join(app.root_path, 'haber', f'{h.id}-{h.slug}.html')
    if os.path.exists(file_path):
        os.remove(file_path)
        
    from flask import flash
    flash('Haber silindi!')
    return redirect(url_for('admin_haber'))
'''

# Remove the stub admin_haber I added earlier
code = re.sub(r'@app\.route\(\'/admin/haber\'\)\n@login_required\ndef admin_haber\(\):\n\s+if not check_editor_permission\(\'haber\'\): return redirect\(url_for\(\'admin_index\'\)\)\n\s+return "Haber page under construction"\n', '', code)


if 'def admin_haber_add():' not in code:
    code = code.replace("if __name__ == '__main__':", haber_routes + "\nif __name__ == '__main__':")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Haber routes added.")
