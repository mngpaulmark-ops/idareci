import os
import re

# 1. Update app.py
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

menu_edit_route = """@app.route('/admin/menu/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_menu_edit(id):
    if not check_editor_permission('menu'): return redirect(url_for('admin_index'))
    menu = Menu.query.get_or_404(id)
    if request.method == 'POST':
        menu.title = request.form.get('title')
        menu.url = request.form.get('url')
        parent_id = request.form.get('parent_id')
        if parent_id and parent_id != '0':
            menu.parent_id = int(parent_id)
        else:
            menu.parent_id = None
        db.session.commit()
        
        import threading
        def bg_update():
            apply_menus_to_all_html()
        threading.Thread(target=bg_update).start()
        
        return redirect(url_for('admin_menu'))
    
    menus = Menu.query.filter_by(parent_id=None).order_by(Menu.order).all()
    return render_template('admin/menu_edit.html', menu=menu, menus=menus)

@app.route('/admin/left_menu/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_left_menu_edit(id):
    if not check_editor_permission('menu'): return redirect(url_for('admin_index'))
    menu = LeftMenu.query.get_or_404(id)
    if request.method == 'POST':
        menu.title = request.form.get('title')
        menu.url = request.form.get('url')
        db.session.commit()
        
        import threading
        def bg_update():
            apply_menus_to_all_html()
        threading.Thread(target=bg_update).start()
        
        return redirect(url_for('admin_left_menu'))
"""

if "def admin_menu_edit" not in code:
    code = code.replace("def admin_menu_delete(id):", menu_edit_route + "\ndef admin_menu_delete(id):")
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(code)

# 2. Add buttons to menu.html
with open('templates/admin/menu.html', 'r', encoding='utf-8') as f:
    m_html = f.read()

m_html = m_html.replace(
    '<a href="{{ url_for(\'admin_menu_move\', id=m.id, dir=\'up\') }}" class="btn btn-sm btn-outline-secondary"><i class="fa fa-arrow-up"></i></a>',
    '<a href="{{ url_for(\'admin_menu_edit\', id=m.id) }}" class="btn btn-sm btn-primary" title="Düzenle"><i class="fa fa-edit"></i></a>\n                                <a href="{{ url_for(\'admin_menu_move\', id=m.id, dir=\'up\') }}" class="btn btn-sm btn-outline-secondary"><i class="fa fa-arrow-up"></i></a>'
)
m_html = m_html.replace(
    '<a href="{{ url_for(\'admin_menu_move\', id=child.id, dir=\'up\') }}" class="btn btn-sm btn-outline-secondary"><i class="fa fa-arrow-up"></i></a>',
    '<a href="{{ url_for(\'admin_menu_edit\', id=child.id) }}" class="btn btn-sm btn-primary" title="Düzenle"><i class="fa fa-edit"></i></a>\n                                        <a href="{{ url_for(\'admin_menu_move\', id=child.id, dir=\'up\') }}" class="btn btn-sm btn-outline-secondary"><i class="fa fa-arrow-up"></i></a>'
)

with open('templates/admin/menu.html', 'w', encoding='utf-8') as f:
    f.write(m_html)

# 3. Add buttons to left_menu.html
with open('templates/admin/left_menu.html', 'r', encoding='utf-8') as f:
    lm_html = f.read()

lm_html = lm_html.replace(
    '<a href="{{ url_for(\'admin_left_menu_move\', id=m.id, dir=\'up\') }}" class="btn btn-sm btn-outline-secondary"><i class="fa fa-arrow-up"></i></a>',
    '<a href="{{ url_for(\'admin_left_menu_edit\', id=m.id) }}" class="btn btn-sm btn-primary" title="Düzenle"><i class="fa fa-edit"></i></a>\n                                <a href="{{ url_for(\'admin_left_menu_move\', id=m.id, dir=\'up\') }}" class="btn btn-sm btn-outline-secondary"><i class="fa fa-arrow-up"></i></a>'
)

with open('templates/admin/left_menu.html', 'w', encoding='utf-8') as f:
    f.write(lm_html)
