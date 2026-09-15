with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

start_idx = app_content.find("def update_sidebar_html():")
end_idx = app_content.find("def update_video_html():")

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
                    f.write(new_page)

"""

app_content = app_content[:start_idx] + new_func + app_content[end_idx:]
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)
print("app.py updated successfully")
