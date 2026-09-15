import re

with open('app.py', 'r', encoding='utf-8', errors='surrogateescape') as f:
    code = f.read()

# Add permission checking helper
permission_helper = """
def check_editor_permission(module):
    if session.get('role') == 'admin': return True
    if session.get('role') == 'editor':
        ed = EditorUser.query.get(session.get('editor_id'))
        if not ed: return False
        if module == 'haber' and ed.can_haber: return True
        if module == 'etkinlik' and ed.can_etkinlik: return True
        if module == 'duyuru' and ed.can_duyuru: return True
        if module == 'kose' and ed.can_kose: return True
    return False
"""

if 'def check_editor_permission' not in code:
    code = code.replace("def login_required(f):", permission_helper + "\ndef login_required(f):")

# Inject permission checks into admin routes
def inject_permission(route_func, module):
    global code
    search = f"def {route_func}():\n"
    if search in code:
        replacement = f"def {route_func}():\n    if not check_editor_permission('{module}'): return redirect(url_for('admin_index'))\n"
        code = code.replace(search, replacement)
    
    search_id = f"def {route_func}(id):\n"
    if search_id in code:
        replacement = f"def {route_func}(id):\n    if not check_editor_permission('{module}'): return redirect(url_for('admin_index'))\n"
        code = code.replace(search_id, replacement)

inject_permission('admin_haber', 'haber')
inject_permission('admin_haber_delete', 'haber')
inject_permission('admin_etkinlik', 'etkinlik')
inject_permission('admin_etkinlik_delete', 'etkinlik')
inject_permission('admin_kose', 'kose')
inject_permission('admin_kose_delete', 'kose')

with open('app.py', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(code)

print("Permissions applied to routes!")
