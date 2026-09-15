import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add column to EditorUser
content = content.replace('can_duyuru = db.Column(db.Boolean, default=False)', 'can_duyuru = db.Column(db.Boolean, default=False)\n    can_kose = db.Column(db.Boolean, default=False)')

# 2. Add form parsing
content = content.replace("cd = request.form.get('can_duyuru') == 'on'", "cd = request.form.get('can_duyuru') == 'on'\n        ck = request.form.get('can_kose') == 'on'")

# 3. Add to 'add' action
content = content.replace('can_etkinlik=ce, can_duyuru=cd))', 'can_etkinlik=ce, can_duyuru=cd, can_kose=ck))')

# 4. Add to 'edit' action
content = content.replace('ed.can_duyuru = cd', 'ed.can_duyuru = cd\n            ed.can_kose = ck')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py to support can_kose.")
