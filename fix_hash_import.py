import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

replacement = """
        editor = EditorUser.query.filter_by(username=username).first()
        from werkzeug.security import check_password_hash
        if editor and check_password_hash(editor.password, password):
"""

code = code.replace("""
        editor = EditorUser.query.filter_by(username=username).first()
        if editor and check_password_hash(editor.password, password):
""", replacement)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed check_password_hash import!")
