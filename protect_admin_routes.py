import re

with open('app.py', 'r', encoding='utf-8', errors='surrogateescape') as f:
    code = f.read()

def inject_admin_only(route_func):
    global code
    search = f"def {route_func}():\n"
    if search in code:
        if "if session.get('role') != 'admin':" not in code:
            replacement = f"def {route_func}():\n    if session.get('role') != 'admin': return redirect(url_for('admin_index'))\n"
            code = code.replace(search, replacement)

inject_admin_only('admin_widgets')
inject_admin_only('admin_sidebar')
inject_admin_only('admin_settings')
inject_admin_only('admin_hesap')
inject_admin_only('admin_menu')
inject_admin_only('admin_left_menu')
inject_admin_only('admin_add')
inject_admin_only('admin_editors')

with open('app.py', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(code)
print("Admin-only protection added to routes.")
