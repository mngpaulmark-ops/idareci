import re

with open('templates/admin/editor_panel.html', 'r', encoding='utf-8') as f:
    code = f.read()

target = """<a href="#" class="btn btn-warning" onclick="alert('Duyuru modülü henüz sistemde bulunmamaktadır. Eklenince buradan erişebilirsiniz.')">Duyurulara Git</a>"""
replacement = """<a href="{{ url_for('admin_duyuru') }}" class="btn btn-warning">Duyurulara Git</a>"""

# Since the file might have 'Duyuru modǬlǬ henǬz...' due to encoding issues earlier, I will use regex
code = re.sub(r'<a href="#" class="btn btn-warning" onclick="alert\([^\)]+\)">Duyurulara Git</a>', replacement, code)

with open('templates/admin/editor_panel.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated editor_panel.html")
