with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

start_idx = app_content.find("def apply_menus_to_all_html():")
if start_idx == -1:
    print("Function not found!")
    exit(1)

next_func_idx = app_content.find("\n@app.route", start_idx + 10)
if next_func_idx == -1:
    next_func_idx = len(app_content)

new_func = """def apply_menus_to_all_html():
    with app.app_context():
        import os
        import re
        menus = Menu.query.filter_by(parent_id=None, is_active=True).order_by(Menu.order).all()
        html = '<ul class="nav navbar-nav">\\n'
        html += '<li class="home"><a href="anasayfa.html"><img alt="Ana Sayfa" src="themes/burokratlar/tema/images/ico-home.png"/></a></li>\\n'
        for m in menus:
            if m.children:
                html += f'<li class="dropdown"><a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="{m.url}" role="button" target="_self">{m.title}</a>\\n<ul class="dropdown-menu" role="menu">\\n'
                for child in [c for c in m.children if c.is_active]: html += f'<li><a href="{child.url}" target="_self">{child.title}</a></li>\\n'
                html += '</ul></li>\\n'
            else:
                html += f'<li><a href="{m.url}" target="_self">{m.title}</a></li>\\n'
        html += '</ul>'
        
        left_menus = LeftMenu.query.filter_by(is_active=True).order_by(LeftMenu.order).all()
        left_html = '<ul id="left-menu">\\n'
        for lm in left_menus: left_html += f'<li><a href="{lm.url}" target="_self">» {lm.title}</a></li>\\n'
        left_html += '</ul>'
        
        files_to_update = []
        for root, dirs, files in os.walk('.'):
            if 'themes' in root or 'templates' in root or '__pycache__' in root or 'instance' in root:
                continue
            for file in files:
                if file.endswith('.html'):
                    files_to_update.append(os.path.join(root, file))
                    
        for file in files_to_update:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f: page = f.read()
            except: continue
            new_page = page
            pattern_top = r'(<nav class="collapse navbar-collapse bs-navbar-collapse" id="bs-example-navbar-collapse-1">\\s*)<ul class="nav navbar-nav">.*?</ul>(\\s*</nav>)'
            new_page = re.sub(pattern_top, r'\\g<1>' + html.replace('\\\\', '\\\\\\\\') + r'\\g<2>', new_page, flags=re.DOTALL)
            pattern_left = r'<ul id="left-menu">.*?</ul>'
            new_page = re.sub(pattern_left, left_html.replace('\\\\', '\\\\\\\\'), new_page, flags=re.DOTALL)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f: f.write(new_page)"""

app_content = app_content[:start_idx] + new_func + app_content[next_func_idx:]
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)
print("Updated apply_menus_to_all_html correctly")
