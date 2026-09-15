import re

with open('app.py', 'r', encoding='utf-8', errors='surrogateescape') as f:
    code = f.read()

# Replace the broken second definition of apply_menus_to_all_html
new_func = """def apply_menus_to_all_html():
    with app.app_context():
        import glob, re
        
        # Build Top Menu HTML
        menus = Menu.query.filter_by(parent_id=None, is_active=True).order_by(Menu.order).all()
        html = '<ul class="nav navbar-nav">\\n'
        html += '<li class="home"><a href="anasayfa.html"><img alt="Ana Sayfa" src="themes/burokratlar/tema/images/ico-home.png"/></a></li>\\n'
        for m in menus:
            if m.children:
                html += f'<li class="dropdown"><a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="{m.url}" role="button" target="_self">{m.title}</a>\\n'
                html += '<ul class="dropdown-menu" role="menu">\\n'
                for child in sorted([c for c in m.children if c.is_active], key=lambda x: x.order):
                    html += f'<li><a href="{child.url}" target="_self">{child.title}</a></li>\\n'
                html += '</ul></li>\\n'
            else:
                html += f'<li><a href="{m.url}" target="_self">{m.title}</a></li>\\n'
        html += '</ul>'

        # Build Left Menu HTML
        left_menus = LeftMenu.query.filter_by(is_active=True).order_by(LeftMenu.order).all()
        left_html = '<div class="list-group" id="left-menu-list">\\n'
        for lm in left_menus:
            left_html += f'<a href="{lm.url}" class="list-group-item">{lm.title}</a>\\n'
        left_html += '</div>'
        
        # We need to find the correct format of the left menu in the HTML files.
        # Actually in HTML it's <ul class="list-none p-0 m-0 text-sm"> or similar? No, the original static files had it as standard <li><a href="...">
        # Let's inspect the actual HTML structure of left menu before applying this indiscriminately.
"""

# I need to know what the left menu looks like in the HTML files before rewriting it!
