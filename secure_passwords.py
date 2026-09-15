import re
import os

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if 'from werkzeug.security import generate_password_hash, check_password_hash' not in content:
    content = content.replace('from werkzeug.utils import secure_filename', 'from werkzeug.utils import secure_filename\nfrom werkzeug.security import generate_password_hash, check_password_hash')

# Update login route logic
old_login = """
        if username == admin_u and password == admin_p:
            session['logged_in'] = True
            session.pop('yazar_id', None)
            session.pop('editor_id', None)
            return redirect(url_for('admin_index'))
            
        yazar = Yazar.query.filter_by(username=username, password=password).first()
        if yazar and yazar.username:
            session['logged_in'] = True
            session['yazar_id'] = yazar.id
            return redirect(url_for('yazar_panel'))
            
        editor = EditorUser.query.filter_by(username=username, password=password).first()
        if editor:
            session['logged_in'] = True
            session.pop('yazar_id', None)
            session['editor_id'] = editor.id
            return redirect(url_for('editor_panel'))
"""

new_login = """
        def is_hashed(p):
            return p and (p.startswith('scrypt:') or p.startswith('pbkdf2:'))

        admin_valid = False
        if username == admin_u:
            if is_hashed(admin_p):
                admin_valid = check_password_hash(admin_p, password)
            elif password == admin_p:
                admin_valid = True
                if not s_pass:
                    db.session.add(Setting(key='admin_pass', value=generate_password_hash(password)))
                else:
                    s_pass.value = generate_password_hash(password)
                db.session.commit()

        if admin_valid:
            session['logged_in'] = True
            session.pop('yazar_id', None)
            session.pop('editor_id', None)
            return redirect(url_for('admin_index'))

        yazar = Yazar.query.filter_by(username=username).first()
        if yazar:
            if is_hashed(yazar.password):
                if check_password_hash(yazar.password, password):
                    session['logged_in'] = True
                    session['yazar_id'] = yazar.id
                    return redirect(url_for('yazar_panel'))
            elif yazar.password == password:
                yazar.password = generate_password_hash(password)
                db.session.commit()
                session['logged_in'] = True
                session['yazar_id'] = yazar.id
                return redirect(url_for('yazar_panel'))

        editor = EditorUser.query.filter_by(username=username).first()
        if editor:
            if is_hashed(editor.password):
                if check_password_hash(editor.password, password):
                    session['logged_in'] = True
                    session.pop('yazar_id', None)
                    session['editor_id'] = editor.id
                    return redirect(url_for('editor_panel'))
            elif editor.password == password:
                editor.password = generate_password_hash(password)
                db.session.commit()
                session['logged_in'] = True
                session.pop('yazar_id', None)
                session['editor_id'] = editor.id
                return redirect(url_for('editor_panel'))
"""

if "def is_hashed(p):" not in content:
    content = content.replace(old_login, new_login)

# Update admin_hesap
old_hesap = """
        if new_p:
            if s_pass: s_pass.value = new_p
            else: db.session.add(Setting(key='admin_pass', value=new_p))
"""
new_hesap = """
        if new_p:
            if s_pass: s_pass.value = generate_password_hash(new_p)
            else: db.session.add(Setting(key='admin_pass', value=generate_password_hash(new_p)))
"""
if "generate_password_hash(new_p)" not in content:
    content = content.replace(old_hesap, new_hesap)

# Update admin_editors add
content = content.replace(
    "db.session.add(EditorUser(username=u, password=p, can_haber=ch, can_etkinlik=ce, can_duyuru=cd))",
    "db.session.add(EditorUser(username=u, password=generate_password_hash(p), can_haber=ch, can_etkinlik=ce, can_duyuru=cd))"
)

# Update admin_editors edit
old_ed_edit = """if p: ed.password = p"""
new_ed_edit = """if p: ed.password = generate_password_hash(p)"""
content = content.replace(old_ed_edit, new_ed_edit)

# Update admin_yazar_ekle
old_yaz_add = """db.session.add(Yazar(name=name, image_path=img_path, username=request.form.get("username"), password=request.form.get("password")))"""
new_yaz_add = """db.session.add(Yazar(name=name, image_path=img_path, username=request.form.get("username"), password=generate_password_hash(request.form.get("password")) if request.form.get("password") else None))"""
content = content.replace(old_yaz_add, new_yaz_add)


with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Passwords secured in app.py")
