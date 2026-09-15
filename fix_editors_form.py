import re

with open('templates/admin/editors_list.html', 'r', encoding='utf-8', errors='surrogateescape') as f:
    html = f.read()

# Add to Add Form
add_fields = """                <div class="mb-3">
                    <label>Şifre</label>
                    <input type="text" name="password" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label>Adı Soyadı</label>
                    <input type="text" name="full_name" class="form-control">
                </div>
                <div class="mb-3">
                    <label>Ünvanı (Örn: Yönetim Kurulu Üyesi)</label>
                    <input type="text" name="title" class="form-control">
                </div>"""
                
html = re.sub(r'<div class="mb-3">\s*<label>.?ifre</label>\s*<input type="text" name="password" class="form-control" required>\s*</div>', add_fields, html)


# Add to Edit Form
edit_fields = """                        <div class="mb-3">
                            <label>Yeni Şifre (Değiştirmek istemiyorsanız boş bırakın)</label>
                            <input type="text" name="password" class="form-control">
                        </div>
                        <div class="mb-3">
                            <label>Adı Soyadı</label>
                            <input type="text" name="full_name" class="form-control" value="{{ ed.full_name or '' }}">
                        </div>
                        <div class="mb-3">
                            <label>Ünvanı</label>
                            <input type="text" name="title" class="form-control" value="{{ ed.title or '' }}">
                        </div>"""

html = re.sub(r'<div class="mb-3">\s*<label>Yeni .?ifre \(De.*?i.*?tirmek istemiyorsan.*?z bo.*? b.*?rak.*?n\)</label>\s*<input type="text" name="password" class="form-control">\s*</div>', edit_fields, html)

with open('templates/admin/editors_list.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html)
print("Updated editors_list.html with full_name and title fields.")
