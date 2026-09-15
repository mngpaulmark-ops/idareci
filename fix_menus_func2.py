import re

with open('app.py', 'r', encoding='utf-8', errors='surrogateescape') as f:
    code = f.read()

new_func = r"""def apply_menus_to_all_html():
    with app.app_context():
        import glob, re
        
        # Build Top Menu HTML
        menus = Menu.query.filter_by(parent_id=None, is_active=True).order_by(Menu.order).all()
        html = '<ul class="nav navbar-nav">\n'
        html += '<li class="home"><a href="anasayfa.html"><img alt="Ana Sayfa" src="themes/burokratlar/tema/images/ico-home.png"/></a></li>\n'
        for m in menus:
            if m.children:
                html += f'<li class="dropdown"><a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="{m.url}" role="button" target="_self">{m.title}</a>\n'
                html += '<ul class="dropdown-menu" role="menu">\n'
                for child in sorted([c for c in m.children if c.is_active], key=lambda x: x.order):
                    html += f'<li><a href="{child.url}" target="_self">{child.title}</a></li>\n'
                html += '</ul></li>\n'
            else:
                html += f'<li><a href="{m.url}" target="_self">{m.title}</a></li>\n'
        html += '</ul>'

        # Build Left Menu HTML
        left_menus = LeftMenu.query.filter_by(is_active=True).order_by(LeftMenu.order).all()
        left_html = '<ul id="left-menu">\n'
        for lm in left_menus:
            left_html += f'    <li><a href="{lm.url}" target="_self"><i class="fa fa-caret-right" style="margin-right:5px; color:#800000;"></i> {lm.title}</a></li>\n'
        left_html += '</ul>'

        for file in glob.glob('*.html') + glob.glob('haber/*.html'):
            try:
                with open(file, 'r', encoding='utf-8', errors='surrogateescape') as f:
                    page = f.read()
                new_page = page
                
                # Replace top menu
                top_pat = r'(<nav[^>]*id="bs-example-navbar-collapse-1"[^>]*>\s*)<ul class="nav navbar-nav">.*?</ul>(\s*</nav>)'
                match = re.search(top_pat, new_page, flags=re.DOTALL)
                if match:
                    new_page = new_page[:match.start()] + match.group(1) + html + match.group(2) + new_page[match.end():]
                
                # Replace left menu
                left_pat = r'<ul id="left-menu">.*?</ul>'
                match = re.search(left_pat, new_page, flags=re.DOTALL)
                if match:
                    new_page = new_page[:match.start()] + left_html + new_page[match.end():]
                
                if new_page != page:
                    with open(file, 'w', encoding='utf-8', errors='surrogateescape') as f:
                        f.write(new_page)
            except Exception as e:
                print(f"Error in {file}: {e}")
"""

# Find the start of the FIRST apply_menus_to_all_html
first_idx = code.find("def apply_menus_to_all_html():")
if first_idx != -1:
    # Find the __main__ block which is at the very end
    main_idx = code.find("if __name__ == '__main__':")
    if main_idx != -1:
        code = code[:first_idx] + new_func + '\n\n' + code[main_idx:]

with open('app.py', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(code)
print("Updated apply_menus_to_all_html manually.")
