import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

replacement = """def admin_index():
    if session.get('role') == 'editor':
        return redirect(url_for('editor_panel'))
    pages = Page.query.order_by(Page.menu_order).all()"""

code = code.replace("""def admin_index():\n    pages = Page.query.order_by(Page.menu_order).all()""", replacement)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Protected admin_index from editors!")
