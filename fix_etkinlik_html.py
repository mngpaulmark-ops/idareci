import re

with open('templates/admin/etkinlik_edit.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                <div class="mb-3">
                    <label class="form-label">Saat (Örn: 14:00)</label>
                    <input type="text" name="saat" class="form-control" value="{{ etkinlik.saat if etkinlik else '' }}">
                </div>"""
                
# Actually since encoding might be messed up with Örn, I will just match on name="saat"
pattern = r'(<input type="text" name="saat" class="form-control" value="\{\{ etkinlik\.saat if etkinlik else \'\' \}\}">\s*</div>)'

replacement = r'\1\n                <div class="mb-3">\n                    <label class="form-label">Yer (Adres/Konum)</label>\n                    <input type="text" name="location" class="form-control" value="{{ etkinlik.location if etkinlik else \'\' }}">\n                </div>'

new_html = re.sub(pattern, replacement, html)

with open('templates/admin/etkinlik_edit.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
    
print("Updated etkinlik_edit.html")
