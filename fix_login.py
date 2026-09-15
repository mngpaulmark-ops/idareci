import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove duplicate imports
while 'from werkzeug.security import generate_password_hash, check_password_hash\nfrom werkzeug.security import generate_password_hash, check_password_hash' in content:
    content = content.replace('from werkzeug.security import generate_password_hash, check_password_hash\nfrom werkzeug.security import generate_password_hash, check_password_hash', 'from werkzeug.security import generate_password_hash, check_password_hash')

# Update login route
pattern = re.compile(r"(\s+)(if username == admin_u and password == admin_p:.*?return redirect\(url_for\('editor_panel'\)\))", re.DOTALL)

new_login = r"""\1def is_hashed(p):
\1    return p and (p.startswith('scrypt:') or p.startswith('pbkdf2:'))
\1
\1admin_valid = False
\1if username == admin_u:
\1    if is_hashed(admin_p):
\1        admin_valid = check_password_hash(admin_p, password)
\1    elif password == admin_p:
\1        admin_valid = True
\1        if not s_pass:
\1            db.session.add(Setting(key='admin_pass', value=generate_password_hash(password)))
\1        else:
\1            s_pass.value = generate_password_hash(password)
\1        db.session.commit()
\1
\1if admin_valid:
\1    session['logged_in'] = True
\1    session.pop('yazar_id', None)
\1    session.pop('editor_id', None)
\1    return redirect(url_for('admin_index'))
\1
\1yazar = Yazar.query.filter_by(username=username).first()
\1if yazar:
\1    if is_hashed(yazar.password):
\1        if check_password_hash(yazar.password, password):
\1            session['logged_in'] = True
\1            session['yazar_id'] = yazar.id
\1            return redirect(url_for('yazar_panel'))
\1    elif yazar.password == password:
\1        yazar.password = generate_password_hash(password)
\1        db.session.commit()
\1        session['logged_in'] = True
\1        session['yazar_id'] = yazar.id
\1        return redirect(url_for('yazar_panel'))
\1
\1editor = EditorUser.query.filter_by(username=username).first()
\1if editor:
\1    if is_hashed(editor.password):
\1        if check_password_hash(editor.password, password):
\1            session['logged_in'] = True
\1            session.pop('yazar_id', None)
\1            session['editor_id'] = editor.id
\1            return redirect(url_for('editor_panel'))
\1    elif editor.password == password:
\1        editor.password = generate_password_hash(password)
\1        db.session.commit()
\1        session['logged_in'] = True
\1        session.pop('yazar_id', None)
\1        session['editor_id'] = editor.id
\1        return redirect(url_for('editor_panel'))
"""

content = pattern.sub(new_login, content)

# update database models to accommodate hashes (String(255))
content = content.replace("password = db.Column(db.String(50)", "password = db.Column(db.String(255)")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated login logic")
