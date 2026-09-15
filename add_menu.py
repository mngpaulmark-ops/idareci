import os

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

menu_model = """
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False, default='#')
    order = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)
    children = db.relationship('Menu', backref=db.backref('parent', remote_side=[id]), order_by='Menu.order')
"""

if 'class Menu(db.Model):' not in code:
    code = code.replace('class Setting(db.Model):', menu_model + '\nclass Setting(db.Model):')

menu_routes = """
@app.route('/admin/menu')
def admin_menu():
    menus = Menu.query.filter_by(parent_id=None).order_by(Menu.order).all()
    return render_template('admin/menu.html', menus=menus)

@app.route('/admin/menu/add', methods=['POST'])
def admin_menu_add():
    title = request.form.get('title')
    url = request.form.get('url')
    parent_id = request.form.get('parent_id', type=int)
    if parent_id == 0: parent_id = None
    
    order = Menu.query.filter_by(parent_id=parent_id).count()
    new_menu = Menu(title=title, url=url, parent_id=parent_id, order=order)
    db.session.add(new_menu)
    db.session.commit()
    
    apply_menus_to_all_html()
    return redirect(url_for('admin_menu'))

@app.route('/admin/menu/delete/<int:id>', methods=['POST'])
def admin_menu_delete(id):
    menu = Menu.query.get_or_404(id)
    # Delete children first
    for child in menu.children:
        db.session.delete(child)
    db.session.delete(menu)
    db.session.commit()
    
    apply_menus_to_all_html()
    return redirect(url_for('admin_menu'))

@app.route('/admin/menu/move/<int:id>/<dir>')
def admin_menu_move(id, dir):
    menu = Menu.query.get_or_404(id)
    # Find sibling
    if dir == 'up':
        sibling = Menu.query.filter_by(parent_id=menu.parent_id).filter(Menu.order < menu.order).order_by(Menu.order.desc()).first()
    else:
        sibling = Menu.query.filter_by(parent_id=menu.parent_id).filter(Menu.order > menu.order).order_by(Menu.order.asc()).first()
        
    if sibling:
        # Swap orders
        menu.order, sibling.order = sibling.order, menu.order
        db.session.commit()
        apply_menus_to_all_html()
        
    return redirect(url_for('admin_menu'))

def apply_menus_to_all_html():
    import glob
    import bs4
    
    # Generate Menu HTML
    menus = Menu.query.filter_by(parent_id=None).order_by(Menu.order).all()
    
    html = '<ul class="nav navbar-nav">\\n'
    html += '<li class="home"><a href="anasayfa.html"><img alt="Ana Sayfa" src="themes/burokratlar/tema/images/ico-home.png"/></a></li>\\n'
    
    for m in menus:
        if m.children:
            html += f'<li class="dropdown"><a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="{m.url}" role="button" target="_self">{m.title}</a>\\n'
            html += '<ul class="dropdown-menu" role="menu">\\n'
            for child in m.children:
                html += f'<li><a href="{child.url}" target="_self">{child.title}</a></li>\\n'
            html += '</ul></li>\\n'
        else:
            html += f'<li><a href="{m.url}" target="_self">{m.title}</a></li>\\n'
            
    html += '</ul>'
    
    for file in glob.glob('*.html') + glob.glob('haber/*.html'):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        soup = bs4.BeautifulSoup(content, 'lxml')
        old_nav = soup.find('ul', class_='nav navbar-nav')
        if old_nav:
            new_nav = bs4.BeautifulSoup(html, 'html.parser')
            old_nav.replace_with(new_nav)
            with open(file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
"""

if 'def admin_menu():' not in code:
    code = code.replace('def admin_settings():', menu_routes + '\ndef admin_settings():')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.py with Menu model")
