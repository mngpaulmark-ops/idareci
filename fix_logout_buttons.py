import re

# 1. Update index.html
with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()
    
target_index = """<div class="container mt-5">
    <h2>Yönetim Paneli - Derneğimiz Sayfaları</h2>"""
    
# In case encoding has weird characters for Yönetim Paneli
pattern_index = r'<div class="container mt-5">\s*<h2>(.*?)</h2>'

replacement_index = r"""<div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h2>\1</h2>
        <a href="{{ url_for('logout') }}" class="btn btn-danger">Çıkış Yap</a>
    </div>"""

new_index = re.sub(pattern_index, replacement_index, index_html)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(new_index)

# 2. Update editor_panel.html
with open('templates/admin/editor_panel.html', 'r', encoding='utf-8') as f:
    editor_html = f.read()

pattern_editor = r'<div class="container mt-5">\s*<h2>(.*?Geldiniz.*?)</h2>\s*<a href="\{\{ url_for\(\'logout\'\) \}\}" class="btn btn-danger.*?</a>'

replacement_editor = r"""<div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>\1</h2>
        <a href="{{ url_for('logout') }}" class="btn btn-danger">Çıkış Yap</a>
    </div>"""

new_editor = re.sub(pattern_editor, replacement_editor, editor_html)

with open('templates/admin/editor_panel.html', 'w', encoding='utf-8') as f:
    f.write(new_editor)
    
print("Updated logout buttons!")
