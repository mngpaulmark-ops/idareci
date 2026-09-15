from app import app, LeftMenu
with app.app_context():
    left_menus = LeftMenu.query.filter_by(is_active=True).order_by(LeftMenu.order).all()
    left_html = '<ul id="left-menu">\n'
    for lm in left_menus: 
        left_html += f'<li><a href="{lm.url}" target="_self">» {lm.title}</a></li>\n'
    left_html += '</ul>'
    print("Generated HTML:")
    print(left_html)
