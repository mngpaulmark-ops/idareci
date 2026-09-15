import re

with open('app.py', 'r', encoding='utf-8', errors='surrogateescape') as f:
    code = f.read()
    
logic = """def admin_index():
    pages = Page.query.order_by(Page.menu_order).all()
    editor = None
    if session.get('role') == 'editor':
        editor = EditorUser.query.get(session.get('editor_id'))
    return render_template('admin/index.html', pages=pages, role=session.get('role'), editor=editor)"""

code = re.sub(
    r'def admin_index\(\):\s*pages = Page\.query\.order_by\(Page\.menu_order\)\.all\(\)\s*return render_template\(\'admin/index\.html\', pages=pages\)',
    logic,
    code
)

with open('app.py', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(code)

print("Patched admin_index in app.py")
