import re

with open('templates/admin/etkinlik_edit.html', 'r', encoding='utf-8', errors='surrogateescape') as f:
    html = f.read()

location_field = """            <div class="mb-3">
                <label>Saat</label>
                <input type="text" name="saat" class="form-control" value="{{ etkinlik.saat if etkinlik else '' }}">
            </div>
            <div class="mb-3">
                <label>Yer (Lokasyon)</label>
                <input type="text" name="location" class="form-control" value="{{ etkinlik.location if etkinlik else '' }}">
            </div>"""

if 'name="location"' not in html:
    html = re.sub(r'<div class="mb-3">\s*<label>Saat</label>\s*<input type="text" name="saat" class="form-control" value="\{\{ etkinlik.saat if etkinlik else \'\' \}\}">\s*</div>', location_field, html)
    
with open('templates/admin/etkinlik_edit.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html)
print("Updated etkinlik_edit.html")
