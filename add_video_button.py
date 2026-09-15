import re

with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'<a href="\{\{ url_for\(\'admin_galeri\'\) \}\}" class="btn btn-primary m-1">Galeri Yönetimi</a>'
replacement = '''<a href="{{ url_for('admin_galeri') }}" class="btn btn-primary m-1">Foto Galeri Yönetimi</a>
                    <a href="{{ url_for('admin_videos') }}" class="btn btn-danger m-1"><i class="bi bi-youtube"></i> Video Galeri Yönetimi</a>'''

new_content = re.sub(pattern, replacement, content)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Added Video Gallery button to admin index.")
