import re

with open('app.py', 'r', encoding='utf-8', errors='surrogateescape') as f:
    code = f.read()
    
# We need to import check_password_hash if not imported
if 'from werkzeug.security import generate_password_hash' in code and 'check_password_hash' not in code:
    code = code.replace('generate_password_hash', 'generate_password_hash, check_password_hash')

# Let's insert EditorUser login logic
editor_login_logic = """
        yazar = Yazar.query.filter_by(username=username, password=password).first()
        if yazar and yazar.username:
            session['logged_in'] = True
            session['yazar_id'] = yazar.id
            session['role'] = 'yazar'
            return redirect(url_for('yazar_panel'))

        editor = EditorUser.query.filter_by(username=username).first()
        if editor and check_password_hash(editor.password, password):
            session['logged_in'] = True
            session['role'] = 'editor'
            session['editor_id'] = editor.id
            return redirect(url_for('admin_index'))
"""

code = re.sub(
    r'yazar = Yazar\.query\.filter_by\(username=username, password=password\)\.first\(\)\s*if yazar and yazar\.username:\s*session\[\'logged_in\'\] = True\s*session\[\'yazar_id\'\] = yazar\.id\s*return redirect\(url_for\(\'yazar_panel\'\)\)',
    editor_login_logic,
    code
)

with open('app.py', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(code)

print("Updated app.py with EditorUser login logic.")
