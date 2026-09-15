import re

with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'<a href="\{\{ url_for\(\'admin_settings\'\) \}\}" class="btn btn-warning m-1">Genel Ayarları</a>'
replacement = '''<a href="{{ url_for('admin_settings') }}" class="btn btn-warning m-1">Genel Ayarları</a>
                    <a href="{{ url_for('admin_widgets') }}" class="btn btn-success m-1">Ön Yüz Widget (Paneller)</a>'''

new_content = re.sub(pattern, replacement, content)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Added Widgets button to admin index.")
