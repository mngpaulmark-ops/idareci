import re

with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'<a href="\{\{ url_for\(\'admin_widgets\'\) \}\}" class="btn btn-success m-1">Ön Yüz Widget \(Paneller\)</a>'
replacement = '''<a href="{{ url_for('admin_widgets') }}" class="btn btn-success m-1">Ön Yüz Widget (Paneller)</a>
                    <a href="{{ url_for('admin_sidebar') }}" class="btn btn-info m-1 text-white">Sol Menü Görünürlükleri</a>'''

new_content = re.sub(pattern, replacement, content)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Added Sidebar Blocks button to admin index.")
