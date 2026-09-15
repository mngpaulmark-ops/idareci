import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace update_sidebar_html
safe_sidebar = '''def update_sidebar_html():
    with app.app_context():
        import glob
        import re
        blocks = {b.slug: b.is_active for b in SidebarBlock.query.all()}
        if not blocks: return
        
        for file in glob.glob('*.html') + glob.glob('haber/*.html') + glob.glob('templates/*.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                page = f.read()
            
            new_page = page
            
            # Simple string replacements for display: none
            for slug, is_active in blocks.items():
                if slug == 'hadis':
                    class_name = 'hadis-i-serif'
                else:
                    class_name = f'side-{slug}'
                    
                # Find the div with this class
                # We assume the div looks like <div class="panel ... side-slug" ... style="...">
                pattern = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*style=")([^"]*)(")'
                
                def replacer(match):
                    pre = match.group(1)
                    style = match.group(2)
                    post = match.group(3)
                    
                    if is_active:
                        style = re.sub(r'display:\s*none\s*!important;?', '', style)
                        style = re.sub(r'display:\s*none;?', '', style)
                    else:
                        if 'display: none' not in style:
                            style += ' display: none !important;'
                    return pre + style.strip() + post
                
                new_page = re.sub(pattern, replacer, new_page)
                
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_page)
'''
start_idx = content.find('def update_sidebar_html():')
if start_idx != -1:
    end_idx = content.find('def update_widgets_html():', start_idx)
    content = content[:start_idx] + safe_sidebar + content[end_idx:]


# Replace update_widgets_html
safe_widgets = '''def update_widgets_html():
    with app.app_context():
        import glob
        import re
        kamu = WidgetContent.query.filter_by(slug='kamu-etigi').first()
        lider = WidgetContent.query.filter_by(slug='yonetim-liderlik').first()
        
        if not kamu or not lider: return
        
        for file in glob.glob('anasayfa.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                page = f.read()
            
            new_page = page
            
            # Very basic string replace for the style attribute of the panel
            for w in [kamu, lider]:
                panel_id = f'panel-{w.slug}'
                
                # Match the style attribute of this specific div
                pattern = r'(<div[^>]*id="' + re.escape(panel_id) + r'"[^>]*style=")([^"]*)(")'
                def replacer(match):
                    pre, style, post = match.groups()
                    if w.is_active:
                        style = re.sub(r'display:\s*none\s*!important;?', '', style)
                        style = re.sub(r'display:\s*none;?', '', style)
                    else:
                        if 'display: none' not in style:
                            style += ' display: none !important;'
                    return pre + style.strip() + post
                
                new_page = re.sub(pattern, replacer, new_page)
                
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_page)
'''
start_idx = content.find('def update_widgets_html():')
if start_idx != -1:
    end_idx = content.find('def get_weather():', start_idx)
    content = content[:start_idx] + safe_widgets + content[end_idx:]

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated update_sidebar_html and update_widgets_html to use regex.")
