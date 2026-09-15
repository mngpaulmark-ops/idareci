import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update model
content = content.replace('link = db.Column(db.String(255))', 'link = db.Column(db.String(255))\n    is_active = db.Column(db.Boolean, default=True)')

# 2. Update admin route saving
pattern = r"lider\.description = request\.form\.get\('lider_desc'\)\n\s+lider\.link = request\.form\.get\('lider_link'\)"
replacement = r"""lider.description = request.form.get('lider_desc')
        lider.link = request.form.get('lider_link')
        
        kamu.is_active = request.form.get('kamu_active') == 'on'
        lider.is_active = request.form.get('lider_active') == 'on'"""
content = re.sub(pattern, replacement, content)

# 3. Update update_widgets_html
html_update_pattern = r"p_kamu = soup\.find\('div', id='panel-kamu-etigi'\)\n\s+if p_kamu:"
html_update_repl = r"""p_kamu = soup.find('div', id='panel-kamu-etigi')
            if p_kamu:
                _toggle_display(p_kamu, kamu.is_active)"""
content = re.sub(html_update_pattern, html_update_repl, content)

html_update_pattern2 = r"p_lider = soup\.find\('div', id='panel-yonetim-liderlik'\)\n\s+if p_lider:"
html_update_repl2 = r"""p_lider = soup.find('div', id='panel-yonetim-liderlik')
            if p_lider:
                _toggle_display(p_lider, lider.is_active)"""
content = re.sub(html_update_pattern2, html_update_repl2, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py with Widget active/passive support.")
