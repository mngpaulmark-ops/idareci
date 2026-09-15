import zipfile
import re

# 1. Restore the ENTIRE old app.py
with zipfile.ZipFile('C:/Users/turga/OneDrive/Desktop/bürokratlar birliği site yedeği/burokratlarbirligi_yedek_14.09.2026.zip') as z:
    app_content = z.read('app.py').decode('utf-8')

# 2. Fix the Haber sorting query
app_content = app_content.replace("Haber.query.order_by(Haber.id.desc()).all()", "Haber.query.order_by(Haber.date.desc(), Haber.id.desc()).all()")
app_content = app_content.replace("Haber.query.order_by(Haber.id.desc()).limit(10).all()", "Haber.query.order_by(Haber.date.desc(), Haber.id.desc()).limit(10).all()")

# 3. Fix the Haber slug and date parsing in admin_haber_add
old_add = """        slug = request.form.get('slug', '')
        if not slug:
            # Generate basic slug
            slug = title.lower().replace(' ', '-').replace('ı', 'i').replace('ö', 'o').replace('ü', 'u').replace('ş', 's').replace('ğ', 'g').replace('ç', 'c')
            slug = "".join(c for c in slug if c.isalnum() or c == '-')
        
        h = Haber(title=title, content=content, slug=slug)
        file = request.files.get('file')"""
new_add = """        slug = request.form.get('slug', '')
        if not slug:
            # Generate basic slug
            slug = title.lower().replace(' ', '-').replace('ı', 'i').replace('ö', 'o').replace('ü', 'u').replace('ş', 's').replace('ğ', 'g').replace('ç', 'c')
            slug = "".join(c for c in slug if c.isalnum() or c == '-')
        
        date_str = request.form.get('date')
        h = Haber(title=title, content=content, slug=slug)
        if date_str:
            import datetime
            try:
                h.date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            except:
                pass
        
        file = request.files.get('image')"""
app_content = app_content.replace(old_add, new_add)

# 4. Fix the Haber slug and date parsing in admin_haber_edit
old_edit = """        h.title = request.form.get('title')
        h.content = request.form.get('content')
        file = request.files.get('file')"""
new_edit = """        h.title = request.form.get('title')
        h.content = request.form.get('content')
        slug = request.form.get('slug')
        if slug:
            h.slug = slug
        date_str = request.form.get('date')
        if date_str:
            import datetime
            try:
                h.date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            except:
                pass
        file = request.files.get('image')"""
app_content = app_content.replace(old_edit, new_edit)

# 5. Fix tracebacks in try/except blocks
app_content = app_content.replace("""        except:
            pass""", """        except Exception as e:
            import traceback
            traceback.print_exc()""")

# 6. Fix `update_sidebar_html` logic (the one that didn't hide things properly)
old_func_sidebar = """def update_sidebar_html():
    with app.app_context():
        import glob, re
        blocks = {b.slug: b.is_active for b in SidebarBlock.query.all()}
        if not blocks: return
        for file in glob.glob('*.html') + glob.glob('haber/*.html'):
            with open(file, 'r', encoding='utf-8', errors='surrogateescape') as f:
                page = f.read()
            new_page = page
            for slug, is_active in blocks.items():
                class_name = 'hadis-i-serif' if slug == 'hadis' else f'side-{slug}'
                pattern = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*style=")([^"]*)(")'
                def make_replacer(active):
                    def replacer(match):
                        return match.group(1) + _toggle_display(match.group(2), active) + match.group(3)
                    return replacer
                new_page = re.sub(pattern, make_replacer(is_active), new_page)
            if new_page != page:
                with open(file, 'w', encoding='utf-8', errors='surrogateescape') as f:
                    f.write(new_page)"""

new_func_sidebar = """def update_sidebar_html():
    with app.app_context():
        import glob, re
        blocks = {b.slug: b.is_active for b in SidebarBlock.query.all()}
        if not blocks: return
        for file in glob.glob('*.html') + glob.glob('haber/*.html'):
            try:
                with open(file, 'r', encoding='utf-8', errors='surrogateescape') as f:
                    page = f.read()
            except: continue
            new_page = page
            for slug, is_active in blocks.items():
                class_name = 'hadis-i-serif' if slug == 'hadis' else f'side-{slug}'
                pattern_no_style = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*)(\\s*)(>)'
                def ensure_style(match):
                    if 'style=' in match.group(1): return match.group(0)
                    return match.group(1) + ' style=""' + match.group(3)
                new_page = re.sub(pattern_no_style, ensure_style, new_page)
                
                pattern = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*style=")([^"]*)(")'
                def make_replacer(active):
                    def replacer(match):
                        return match.group(1) + _toggle_display(match.group(2), active) + match.group(3)
                    return replacer
                new_page = re.sub(pattern, make_replacer(is_active), new_page)
            if new_page != page:
                with open(file, 'w', encoding='utf-8', errors='surrogateescape') as f:
                    f.write(new_page)"""
if old_func_sidebar in app_content:
    app_content = app_content.replace(old_func_sidebar, new_func_sidebar)

# 7. Fix `apply_menus_to_all_html`
# Find exactly where it is so we don't truncate
start_idx = app_content.find("def apply_menus_to_all_html():")
# We know admin_haber follows apply_menus_to_all_html in the original backup
end_idx = app_content.find("@app.route('/admin/haber')", start_idx)

new_apply_menus = """def apply_menus_to_all_html():
    with app.app_context():
        import glob
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
        
        for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f: page = f.read()
            except: continue
            new_page = page
            pattern_top = r'(<nav class="collapse navbar-collapse bs-navbar-collapse" id="bs-example-navbar-collapse-1">\\s*)<ul class="nav navbar-nav">.*?</ul>(\\s*</nav>)'
            new_page = re.sub(pattern_top, r'\\g<1>' + html.replace('\\\\', '\\\\\\\\') + r'\\g<2>', new_page, flags=re.DOTALL)
            pattern_left = r'(<div class="panel-heading">\\s*<img alt="Menu" src="themes/burokratlar/tema/images/icon-menu.png"/> Derneğimiz\\s*</div>\\s*<div class="panel-body">\\s*)<ul id="left-menu">.*?</ul>(\\s*</div>)'
            new_page = re.sub(pattern_left, r'\\g<1>' + left_html.replace('\\\\', '\\\\\\\\') + r'\\g<2>', new_page, flags=re.DOTALL)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f: f.write(new_page)

"""
if start_idx != -1 and end_idx != -1:
    app_content = app_content[:start_idx] + new_apply_menus + app_content[end_idx:]

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("Safely fully restored and patched app.py")
