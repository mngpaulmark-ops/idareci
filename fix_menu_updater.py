import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

safe_menus_inner = '''def _apply_menus_inner():
    import glob
    import re
    
    # Generate Top Menu HTML
    menus = Menu.query.filter_by(parent_id=None, is_active=True).order_by(Menu.order).all()
    
    html = '<ul class="nav navbar-nav">\\n'
    html += '<li class="home"><a href="anasayfa.html"><img alt="Ana Sayfa" src="themes/burokratlar/tema/images/ico-home.png"/></a></li>\\n'
    
    for m in menus:
        if m.children:
            html += f'<li class="dropdown"><a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="{m.url}" role="button" target="_self">{m.title}</a>\\n'
            html += '<ul class="dropdown-menu" role="menu">\\n'
            for child in [c for c in m.children if c.is_active]:
                html += f'<li><a href="{child.url}" target="_self">{child.title}</a></li>\\n'
            html += '</ul></li>\\n'
        else:
            html += f'<li><a href="{m.url}" target="_self">{m.title}</a></li>\\n'
            
    html += '</ul>'
    
    # Generate Left Menu HTML
    left_menus = LeftMenu.query.filter_by(is_active=True).order_by(LeftMenu.order).all()
    left_html = '<ul id="left-menu">\\n'
    for lm in left_menus:
        left_html += f'<li><a href="{lm.url}" target="_self">{lm.title}</a></li>\\n'
    left_html += '</ul>'
    
    for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            page = f.read()
            
        new_page = page
        
        # Replace top menu
        pattern_top = r'(<nav class="collapse navbar-collapse bs-navbar-collapse" id="bs-example-navbar-collapse-1">\\s*)<ul class="nav navbar-nav">.*?</ul>(\\s*</nav>)'
        new_page = re.sub(pattern_top, r'\\g<1>' + html.replace('\\\\', '\\\\\\\\') + r'\\g<2>', new_page, flags=re.DOTALL)
        
        # Replace left menu inside panel-primary
        pattern_left = r'(<div class="panel-heading">\\s*<img alt="Menu" src="themes/burokratlar/tema/images/icon-menu.png"/> Derneğimiz\\s*</div>\\s*<div class="panel-body">\\s*)<ul id="left-menu">.*?</ul>(\\s*</div>)'
        new_page = re.sub(pattern_left, r'\\g<1>' + left_html.replace('\\\\', '\\\\\\\\') + r'\\g<2>', new_page, flags=re.DOTALL)
        
        if new_page != page:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_page)
'''

# Use manual string replacement
start_idx = content.find('def _apply_menus_inner():')
if start_idx != -1:
    end_idx = content.find('def apply_side_links_to_all_html():', start_idx)
    if end_idx == -1: end_idx = len(content)
    
    new_content = content[:start_idx] + safe_menus_inner + '\n\n' + content[end_idx:]
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated _apply_menus_inner via string replace.")
else:
    print("Could not find _apply_menus_inner")
