import re

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_func = re.search(r'def apply_menus_to_all_html\(\):.*?(?=\n@|\Z)', text, re.DOTALL)
if old_func:
    new_func = '''def apply_menus_to_all_html():
    import glob
    import bs4
    
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
        left_html += f'<li><a href="{lm.url}" target="_self">» {lm.title}</a></li>\\n'
    left_html += '</ul>'
    
    for file in glob.glob('*.html') + glob.glob('haber/*.html'):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        soup = bs4.BeautifulSoup(content, 'lxml')
        
        changed = False
        
        old_nav = soup.find('ul', class_='nav navbar-nav')
        if old_nav:
            new_nav = bs4.BeautifulSoup(html, 'html.parser')
            old_nav.replace_with(new_nav)
            changed = True
            
        old_left = soup.find('ul', id='left-menu')
        if old_left:
            new_left = bs4.BeautifulSoup(left_html, 'html.parser')
            old_left.replace_with(new_left)
            changed = True
            
        if changed:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(str(soup))'''
    
    text = text.replace(old_func.group(0), new_func)
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated apply_menus_to_all_html')
