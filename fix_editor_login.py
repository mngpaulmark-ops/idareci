import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Inject EditorUser login check
login_check = """
        editor = EditorUser.query.filter_by(username=username).first()
        if editor and check_password_hash(editor.password, password):
            session['logged_in'] = True
            session['role'] = 'editor'
            session['editor_id'] = editor.id
            session.pop('yazar_id', None)
            return redirect(url_for('editor_panel'))
            
        yazar = Yazar.query.filter_by(username=username, password=password).first()"""
code = code.replace("yazar = Yazar.query.filter_by(username=username, password=password).first()", login_check)


# 2. Add editor_panel route
editor_route = """
@app.route('/editor_panel')
@login_required
def editor_panel():
    if session.get('role') != 'editor':
        return redirect(url_for('admin_index'))
    editor = EditorUser.query.get(session.get('editor_id'))
    if not editor:
        return redirect(url_for('logout'))
    return render_template('admin/editor_panel.html', editor=editor)

@app.route('/admin')"""

code = code.replace("@app.route('/admin')", editor_route)

# Make sure check_password_hash is imported!
if 'check_password_hash' not in code:
    code = code.replace("from werkzeug.security import generate_password_hash", "from werkzeug.security import generate_password_hash, check_password_hash")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Added EditorUser login and route to app.py")
