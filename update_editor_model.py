import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Model
model_repl = '''class EditorUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))
    title = db.Column(db.String(100))
    role = db.Column(db.String(100))
    can_haber = db.Column(db.Boolean, default=False)'''

content = re.sub(r'class EditorUser\(db\.Model\):\n\s+id =.*?\n\s+username =.*?\n\s+password =.*?\n\s+can_haber = db\.Column\(db\.Boolean, default=False\)', model_repl, content, flags=re.DOTALL)

# Update admin_editors add logic
add_repl = '''
        fn = request.form.get('full_name')
        ti = request.form.get('title')
        ro = request.form.get('role')
        
        if action == 'add':
            db.session.add(EditorUser(
                username=u, password=generate_password_hash(p), 
                full_name=fn, title=ti, role=ro,
                can_haber=ch, can_etkinlik=ce, can_duyuru=cd, can_kose=ck))
'''
content = re.sub(r"if action == 'add':\n\s+db\.session\.add\(EditorUser\(username=u, password=generate_password_hash\(p\), can_haber=ch, can_etkinlik=ce, can_duyuru=cd, can_kose=ck\)\)", add_repl, content)

# Update admin_editors edit logic
edit_repl = '''elif action == 'edit':
            eid = request.form.get('editor_id')
            ed = EditorUser.query.get(eid)
            ed.username = u
            ed.full_name = fn
            ed.title = ti
            ed.role = ro
            if p: ed.password = generate_password_hash(p)'''
content = re.sub(r"elif action == 'edit':\n\s+eid = request\.form\.get\('editor_id'\)\n\s+ed = EditorUser\.query\.get\(eid\)\n\s+ed\.username = u\n\s+if p: ed\.password = generate_password_hash\(p\)", edit_repl, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py with full_name, title, and role.")
