import re

def update_sidebar_html_fixed():
    import glob
    from app import app, SidebarBlock, _toggle_display
    
    with app.app_context():
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
                
                # First, ensure the div HAS a style attribute
                # Find the div without a style attribute
                pattern_no_style = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*)(\s*)(>)'
                
                def ensure_style(match):
                    # if style= is already in match.group(1), do nothing
                    if 'style=' in match.group(1):
                        return match.group(0)
                    else:
                        return match.group(1) + ' style=""' + match.group(3)
                
                new_page = re.sub(pattern_no_style, ensure_style, new_page)
                
                # Now it definitely has a style attribute, use the old regex
                pattern = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*style=")([^"]*)(")'
                def make_replacer(active):
                    def replacer(match):
                        return match.group(1) + _toggle_display(match.group(2), active) + match.group(3)
                    return replacer
                new_page = re.sub(pattern, make_replacer(is_active), new_page)
                
            if new_page != page:
                with open(file, 'w', encoding='utf-8', errors='surrogateescape') as f:
                    f.write(new_page)

# Update app.py's update_sidebar_html function
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

import ast
# We will just string replace the body of update_sidebar_html
old_func = """def update_sidebar_html():
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

new_func = """def update_sidebar_html():
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
                pattern_no_style = r'(<div[^>]*class="[^"]*' + re.escape(class_name) + r'[^"]*"[^>]*)(\s*)(>)'
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

if old_func in app_content:
    app_content = app_content.replace(old_func, new_func)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("Replaced successfully in app.py")
else:
    print("Could not find exact old function string.")

# Run it once right now to fix the site
update_sidebar_html_fixed()
print("Ran update_sidebar_html_fixed()")
