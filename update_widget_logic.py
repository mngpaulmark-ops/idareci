import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

safe_update = """def update_widgets_html():
    with app.app_context():
        import glob, re
        kamu = WidgetContent.query.filter_by(slug='kamu-etigi').first()
        lider = WidgetContent.query.filter_by(slug='yonetim-liderlik').first()
        if not kamu or not lider: return

        for file in glob.glob('anasayfa.html'):
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                page = f.read()
            
            new_page = page
            for w in [kamu, lider]:
                panel_id = f'panel-{w.slug}'
                
                # Regex to match the opening div tag completely
                pattern = r'(<div[^>]*id="' + re.escape(panel_id) + r'"[^>]*>)'
                
                def make_replacer(widget):
                    def replacer(match):
                        tag = match.group(1)
                        if 'style="' in tag:
                            # Replace existing style
                            if widget.is_active:
                                tag = re.sub(r'style="([^"]*display:\s*none\s*!important;?[^"]*)"', r'style=""', tag)
                            else:
                                tag = re.sub(r'style="([^"]*)"', r'style="\1 display: none !important;"', tag)
                        else:
                            # Insert style
                            if not widget.is_active:
                                tag = tag.replace('>', ' style="display: none !important;">', 1)
                        return tag
                    return replacer

                new_page = re.sub(pattern, make_replacer(w), new_page)
                
            if new_page != page:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_page)
"""

start_idx = code.find('def update_widgets_html():')
if start_idx != -1:
    end_idx = code.find('def update_sidebar_html():', start_idx)
    if end_idx == -1: end_idx = len(code)
    
    new_code = code[:start_idx] + safe_update + "\n\n" + code[end_idx:]
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("Updated update_widgets_html to handle tags without style attribute")
else:
    print("Could not find update_widgets_html")
