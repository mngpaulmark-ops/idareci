import re
from app import app, LeftMenu

with app.app_context():
    left_menus = LeftMenu.query.filter_by(is_active=True).order_by(LeftMenu.order).all()
    left_html = '<ul id="left-menu">\n'
    for lm in left_menus: left_html += f'<li><a href="{lm.url}" target="_self">» {lm.title}</a></li>\n'
    left_html += '</ul>'

    with open('anasayfa.html', 'r', encoding='utf-8', errors='ignore') as f:
        page = f.read()
    
    pattern_left = r'<ul id="left-menu">.*?</ul>'
    new_page = re.sub(pattern_left, left_html.replace('\\', '\\\\'), page, flags=re.DOTALL)
    
    print("Same?:", new_page == page)
    if new_page != page:
        print("Saving...")
        with open('anasayfa.html', 'w', encoding='utf-8') as f:
            f.write(new_page)
        print("Saved!")
