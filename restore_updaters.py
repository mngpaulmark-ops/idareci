import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

funcs_to_add = '''
def update_widgets_html():
    with app.app_context():
        import glob
        import re
        kamu = WidgetContent.query.filter_by(slug='kamu-etigi').first()
        lider = WidgetContent.query.filter_by(slug='yonetim-liderlik').first()
        if not kamu or not lider: return
        for file in glob.glob('anasayfa.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f: page = f.read()
            new_page = page
            for w in [kamu, lider]:
                panel_id = f'panel-{w.slug}'
                pattern = r'(<div[^>]*id="' + re.escape(panel_id) + r'"[^>]*style=")([^"]*)(")'
                def replacer(match, is_active=w.is_active):
                    pre, style, post = match.groups()
                    if is_active:
                        style = re.sub(r'display:\s*none\s*!important;?', '', style)
                        style = re.sub(r'display:\s*none;?', '', style)
                    else:
                        if 'display: none' not in style: style += ' display: none !important;'
                    return pre + style.strip() + post
                new_page = re.sub(pattern, replacer, new_page)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f: f.write(new_page)

def update_sidebar_html():
    with app.app_context():
        import glob
        import re
        blocks = {b.slug: b.is_active for b in SidebarBlock.query.all()}
        if not blocks: return
        for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f: page = f.read()
            new_page = page
            for slug, is_active in blocks.items():
                class_name = 'hadis-i-serif' if slug == 'hadis' else f'side-{slug}'
                pattern = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*style=")([^"]*)(")'
                def make_replacer(active):
                    def replacer(match):
                        pre, style, post = match.groups()
                        if active:
                            style = re.sub(r'display:\s*none\s*!important;?', '', style)
                            style = re.sub(r'display:\s*none;?', '', style)
                        else:
                            if 'display: none' not in style: style += ' display: none !important;'
                        return pre + style.strip() + post
                    return replacer
                new_page = re.sub(pattern, make_replacer(is_active), new_page)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f: f.write(new_page)

def update_video_html():
    with app.app_context():
        import glob
        import re
        videos = Video.query.order_by(Video.order).all()
        if not videos: return
        html = ""
        for v in videos:
            html += f"<li><div style='padding: 5px; text-align:center;'>{v.embed_code}<div class='caption' style='margin-top:5px;'><h5 style='font-size:13px; font-weight:bold; color:#333;'>{v.title}</h5></div></div></li>\\n"
        for file in glob.glob('anasayfa.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f: page = f.read()
            pattern = r'(<div class="panel-body videogaleri jcarousel">.*?<ul>).*?(</ul>\\s*</div>)'
            new_page = re.sub(pattern, r'\\g<1>\\n' + html.replace('\\\\', '\\\\\\\\') + r'\\g<2>', page, flags=re.DOTALL)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f: f.write(new_page)

def apply_menus_to_all_html():
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
        for lm in left_menus: left_html += f'<li><a href="{lm.url}" target="_self">{lm.title}</a></li>\\n'
        left_html += '</ul>'
        
        for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f: page = f.read()
            new_page = page
            pattern_top = r'(<nav class="collapse navbar-collapse bs-navbar-collapse" id="bs-example-navbar-collapse-1">\\s*)<ul class="nav navbar-nav">.*?</ul>(\\s*</nav>)'
            new_page = re.sub(pattern_top, r'\\g<1>' + html.replace('\\\\', '\\\\\\\\') + r'\\g<2>', new_page, flags=re.DOTALL)
            pattern_left = r'(<div class="panel-heading">\\s*<img alt="Menu" src="themes/burokratlar/tema/images/icon-menu.png"/> Derneğimiz\\s*</div>\\s*<div class="panel-body">\\s*)<ul id="left-menu">.*?</ul>(\\s*</div>)'
            new_page = re.sub(pattern_left, r'\\g<1>' + left_html.replace('\\\\', '\\\\\\\\') + r'\\g<2>', new_page, flags=re.DOTALL)
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f: f.write(new_page)

'''

if 'def update_widgets_html():' not in code:
    code = code.replace("if __name__ == '__main__':", funcs_to_add + "\nif __name__ == '__main__':")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Added updater functions.")
