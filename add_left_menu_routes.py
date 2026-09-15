import re

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_routes = '''

@app.route('/admin/left_menu')
@login_required
def admin_left_menu():
    menus = LeftMenu.query.order_by(LeftMenu.order).all()
    return render_template('admin/left_menu.html', menus=menus)

@app.route('/admin/left_menu/add', methods=['POST'])
@login_required
def admin_left_menu_add():
    title = request.form.get('title')
    url = request.form.get('url', '#')
    if title:
        last = LeftMenu.query.order_by(LeftMenu.order.desc()).first()
        order = last.order + 1 if last else 0
        menu = LeftMenu(title=title, url=url, order=order)
        db.session.add(menu)
        db.session.commit()
        apply_menus_to_all_html()
        flash("Sol menü başarıyla eklendi.")
    return redirect(url_for('admin_left_menu'))

@app.route('/admin/left_menu/toggle/<int:id>', methods=['POST'])
@login_required
def admin_left_menu_toggle(id):
    menu = LeftMenu.query.get_or_404(id)
    menu.is_active = not menu.is_active
    db.session.commit()
    apply_menus_to_all_html()
    flash(f"Sol menü {'aktif' if menu.is_active else 'pasif'} duruma getirildi.")
    return redirect(url_for('admin_left_menu'))

@app.route('/admin/left_menu/delete/<int:id>', methods=['POST'])
@login_required
def admin_left_menu_delete(id):
    menu = LeftMenu.query.get_or_404(id)
    db.session.delete(menu)
    db.session.commit()
    apply_menus_to_all_html()
    flash("Sol menü silindi.")
    return redirect(url_for('admin_left_menu'))

@app.route('/admin/left_menu/move/<int:id>/<dir>')
@login_required
def admin_left_menu_move(id, dir):
    menu = LeftMenu.query.get_or_404(id)
    if dir == 'up':
        other = LeftMenu.query.filter(LeftMenu.order < menu.order).order_by(LeftMenu.order.desc()).first()
    else:
        other = LeftMenu.query.filter(LeftMenu.order > menu.order).order_by(LeftMenu.order.asc()).first()
        
    if other:
        menu.order, other.order = other.order, menu.order
        db.session.commit()
        apply_menus_to_all_html()
    return redirect(url_for('admin_left_menu'))

@app.route('/admin/settings', methods=['GET', 'POST'])
'''

text = text.replace("@app.route('/admin/settings', methods=['GET', 'POST'])", new_routes)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Added left menu routes')
