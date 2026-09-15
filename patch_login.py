import os

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace login logic
old_login = "if username == 'admin' and password == '123456':"
new_login = """
        admin_u = Setting.query.filter_by(key='admin_username').first()
        admin_p = Setting.query.filter_by(key='admin_password').first()
        valid_u = admin_u.value if admin_u else 'admin'
        valid_p = admin_p.value if admin_p else '123456'
        
        if username == valid_u and password == valid_p:
"""
text = text.replace(old_login, new_login)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patched login")
