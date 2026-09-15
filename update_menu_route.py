with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

route_str = """
@app.route('/admin/menu/toggle/<int:id>', methods=['POST'])
@login_required
def admin_menu_toggle(id):
    menu = Menu.query.get_or_404(id)
    menu.is_active = not menu.is_active
    db.session.commit()
    apply_menus_to_all_html()
    flash(f"Menü {'aktif' if menu.is_active else 'pasif'} duruma getirildi.")
    return redirect(url_for('admin_menu'))

@app.route('/admin/menu/delete/<int:id>', methods=['POST'])
"""
text = text.replace("@app.route('/admin/menu/delete/<int:id>', methods=['POST'])", route_str.strip())

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Added menu toggle route')
